from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
import odoo
from odoo.service import db
from odoo.http import request

from werkzeug import urls
from datetime import timedelta

import datetime
import os
import json
import requests
import tempfile
import errno
import logging

_logger = logging.getLogger(__name__)

GOOGLE_AUTH_ENDPOINT = 'https://accounts.google.com/o/oauth2/auth'
GOOGLE_TOKEN_ENDPOINT = 'https://accounts.google.com/o/oauth2/token'
GOOGLE_API_BASE_URL = 'https://www.googleapis.com'


class AutoDatabaseBackup(models.Model):
    _name = 'db.backup.configure'
    _description = 'Automatic Database Backup'

    name = fields.Char(string='Name', required=True)
    db_name = fields.Char(string='Database Name', required=True)
    master_pwd = fields.Char(string='Master Password', required=True)
    backup_format = fields.Selection([
        ('zip', 'Zip'),
        ('dump', 'Dump')
    ], string='Backup Format', default='zip', required=True)
    backup_destination = fields.Selection([
        ('local', 'Local Storage'),
        ('google_drive', 'Google Drive'),
    ], string='Backup Destination')
    backup_path = fields.Char(string='Backup Path', help='Local storage directory path')
    
    active = fields.Boolean(default=True)
    auto_remove = fields.Boolean(string='Remove Old Backups')
    days_to_remove = fields.Integer(string='Remove After',
                                    help='Automatically delete stored backups after this specified number of days')
    google_drive_folderid = fields.Char(string='Drive Folder ID')
    notify_user = fields.Boolean(string='Notify User',
                                 help='Send an email notification to user when the backup operation is successful or failed')
    user_id = fields.Many2one('res.users', string='User')
    backup_filename = fields.Char(string='Backup Filename', help='For Storing generated backup filename')
    generated_exception = fields.Char(string='Exception', help='Exception Encountered while Backup generation')
    
    gdrive_refresh_token = fields.Char(string='Google drive Refresh Token', copy=False)
    gdrive_access_token = fields.Char(string='Google Drive Access Token', copy=False)
    is_google_drive_token_generated = fields.Boolean(string='Google drive Token Generated',
                                                     compute='_compute_is_google_drive_token_generated', copy=False)
    gdrive_client_id = fields.Char(string='Google Drive Client ID', copy=False)
    gdrive_client_secret = fields.Char(string='Google Drive Client Secret', copy=False)
    gdrive_token_validity = fields.Datetime(string='Google Drive Token Validity', copy=False)
    gdrive_redirect_uri = fields.Char(string='Google Drive Redirect URI', compute='_compute_redirect_uri')

    def _compute_redirect_uri(self):
        for rec in self:
            base_url = request.env['ir.config_parameter'].get_param('web.base.url')
            rec.gdrive_redirect_uri = base_url + '/google_drive/authentication'


    @api.depends('gdrive_access_token', 'gdrive_refresh_token')
    def _compute_is_google_drive_token_generated(self):
        """
        Set True if the Google Drive refresh token is generated
        """
        for rec in self:
            rec.is_google_drive_token_generated = bool(rec.gdrive_access_token) and bool(rec.gdrive_refresh_token)

    def action_get_gdrive_auth_code(self):
        """
        Generate ogoogle drive authorization code
        """
        action = self.env["ir.actions.act_window"].sudo()._for_xml_id("auto_database_backup.action_db_backup_configure")
        base_url = request.env['ir.config_parameter'].get_param('web.base.url')
        url_return = base_url + '/web#id=%d&action=%d&view_type=form&model=%s' % (self.id, action['id'], 'db.backup.configure')
        state = {
            'backup_config_id': self.id,
            'url_return': url_return
        }
        encoded_params = urls.url_encode({
            'response_type': 'code',
            'client_id': self.gdrive_client_id,
            'scope': 'https://www.googleapis.com/auth/drive https://www.googleapis.com/auth/drive.file',
            'redirect_uri': base_url + '/google_drive/authentication',
            'access_type': 'offline',
            'state': json.dumps(state),
            'approval_prompt': 'force',
        })
        auth_url = "%s?%s" % (GOOGLE_AUTH_ENDPOINT, encoded_params)
        return {
            'type': 'ir.actions.act_url',
            'target': 'self',
            'url': auth_url,
        }


    def generate_gdrive_refresh_token(self):
        """
        generate google drive access token from refresh token if expired
        """
        headers = {"content-type": "application/x-www-form-urlencoded"}
        data = {
            'refresh_token': self.gdrive_refresh_token,
            'client_id': self.gdrive_client_id,
            'client_secret': self.gdrive_client_secret,
            'grant_type': 'refresh_token',
        }
        try:
            res = requests.post(GOOGLE_TOKEN_ENDPOINT, data=data, headers=headers)
            res.raise_for_status()
            response = res.content and res.json() or {}
            if response:
                expires_in = response.get('expires_in')
                self.write({
                    'gdrive_access_token': response.get('access_token'),
                    'gdrive_token_validity': fields.Datetime.now() + timedelta(seconds=expires_in) if expires_in else False,
                })
        except requests.HTTPError as error:
            error_key = error.response.json().get("error", "nc")
            error_msg = _(
                "An error occurred while generating the token. Your authorization code may be invalid or has already expired [%s]. "
                "You should check your Client ID and secret on the Google APIs plateform or try to stop and restart your calendar synchronisation.",
                error_key)
            raise UserError(error_msg)

    def get_gdrive_tokens(self, authorize_code):
        """
        Generate onedrive tokens from authorization code
        """

        base_url = request.env['ir.config_parameter'].get_param('web.base.url')

        headers = {"content-type": "application/x-www-form-urlencoded"}
        data = {
            'code': authorize_code,
            'client_id': self.gdrive_client_id,
            'client_secret': self.gdrive_client_secret,
            'grant_type': 'authorization_code',
            'redirect_uri': base_url + '/google_drive/authentication'
        }
        try:
            res = requests.post(GOOGLE_TOKEN_ENDPOINT, params=data,
                                headers=headers)
            res.raise_for_status()
            response = res.content and res.json() or {}
            if response:
                expires_in = response.get('expires_in')
                self.write({
                    'gdrive_access_token': response.get('access_token'),
                    'gdrive_refresh_token': response.get('refresh_token'),
                    'gdrive_token_validity': fields.Datetime.now() + timedelta(
                        seconds=expires_in) if expires_in else False,
                })
        except requests.HTTPError:
            error_msg = _("Something went wrong during your token generation. Maybe your Authorization Code is invalid")
            raise UserError(error_msg)


    @api.constrains('db_name')
    def _check_db_credentials(self):
        """
        Validate entered database name and master password
        """
        database_list = db.list_dbs()
        if self.db_name not in database_list:
            raise ValidationError(_("Invalid Database Name!"))
        try:
            odoo.service.db.check_super(self.master_pwd)
        except Exception:
            raise ValidationError(_("Invalid Master Password!"))

    def _schedule_auto_backup(self):
        """
        Function for generating and storing backup
        Database backup for all the active records in backup configuration model will be created
        """
        records = self.search([])
        mail_template_success = self.env.ref('auto_database_backup.mail_template_data_db_backup_successful')
        mail_template_failed = self.env.ref('auto_database_backup.mail_template_data_db_backup_failed')
        for rec in records:
            backup_time = datetime.datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")
            backup_filename = "%s_%s.%s" % (rec.db_name, backup_time, rec.backup_format)
            rec.backup_filename = backup_filename
            # Local backup
            if rec.backup_destination == 'local':
                try:
                    if not os.path.isdir(rec.backup_path):
                        os.makedirs(rec.backup_path)
                    backup_file = os.path.join(rec.backup_path, backup_filename)
                    f = open(backup_file, "wb")
                    odoo.service.db.dump_db(rec.db_name, f, rec.backup_format)
                    f.close()
                    # remove older backups
                    if rec.auto_remove:
                        for filename in os.listdir(rec.backup_path):
                            file = os.path.join(rec.backup_path, filename)
                            create_time = datetime.datetime.fromtimestamp(os.path.getctime(file))
                            backup_duration = datetime.datetime.utcnow() - create_time
                            if backup_duration.days >= rec.days_to_remove:
                                os.remove(file)
                    if rec.notify_user:
                        mail_template_success.send_mail(rec.id, force_send=True)
                except Exception as e:
                    rec.generated_exception = e
                    _logger.info('FTP Exception: %s', e)
                    if rec.notify_user:
                        mail_template_failed.send_mail(rec.id, force_send=True)
            # Google Drive backup
            elif rec.backup_destination == 'google_drive':
                if rec.gdrive_token_validity <= fields.Datetime.now():
                    rec.generate_gdrive_refresh_token()
                temp = tempfile.NamedTemporaryFile(suffix='.%s' % rec.backup_format)
                with open(temp.name, "wb+") as tmp:
                    odoo.service.db.dump_db(rec.db_name, tmp, rec.backup_format)
                try:
                    # access_token = self.env['google.drive.config'].sudo().get_access_token()
                    headers = {"Authorization": "Bearer %s" % rec.gdrive_access_token}
                    para = {
                        "name": backup_filename,
                        "parents": [rec.google_drive_folderid],
                    }
                    files = {
                        'data': ('metadata', json.dumps(para), 'application/json; charset=UTF-8'),
                        'file': open(temp.name, "rb")
                    }
                    requests.post(
                        "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
                        headers=headers,
                        files=files
                    )
                    if rec.auto_remove:
                        query = "parents = '%s'" % rec.google_drive_folderid
                        files_req = requests.get("https://www.googleapis.com/drive/v3/files?q=%s" % query, headers=headers)
                        files = files_req.json()['files']
                        for file in files:
                            file_date_req = requests.get("https://www.googleapis.com/drive/v3/files/%s?fields=createdTime" % file['id'], headers=headers)
                            create_time = file_date_req.json()['createdTime'][:19].replace('T', ' ')
                            diff_days = (datetime.datetime.now() - datetime.datetime.strptime(create_time, '%Y-%m-%d %H:%M:%S')).days
                            if diff_days >= rec.days_to_remove:
                                requests.delete("https://www.googleapis.com/drive/v3/files/%s" % file['id'], headers=headers)
                    if rec.notify_user:
                        mail_template_success.send_mail(rec.id, force_send=True)
                except Exception as e:
                    rec.generated_exception = e
                    _logger.info('Google Drive Exception: %s', e)
                    if rec.notify_user:
                        mail_template_failed.send_mail(rec.id, force_send=True)