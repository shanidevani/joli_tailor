from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    # Shirt map
    shirt_length = fields.Char(string="Shirt Length")
    shirt_shoulder = fields.Char(string="Shirt Shoulder")
    shirt_sleeve_length = fields.Char(string="Shirt Sleeve Length")
    shirt_sleeve_length1 = fields.Char()
    shirt_sleeve_length2 = fields.Char()
    shirt_chest = fields.Char(string="Shirt Chest")
    shirt_half_sleeve = fields.Char()
    shirt_half_sleeve_patti = fields.Selection([
        ('Simple', 'Simple'),
        ('Patti', 'Patti')], string="Sleeve Patti", copy=False)
    shirt_petch = fields.Char(string="Petch")
    shirt_petch1 = fields.Char()
    shirt_petch2 = fields.Char()
    shirt_pet = fields.Char(string="Shirt Pet")
    shirt_cuff = fields.Char(string="Shirt Cuff")
    shirt_seat = fields.Char(string="Shirt Seat")
    open_shirt = fields.Selection([
        ('Open', 'Open'),
        ('Bushirt', 'Bushirt')
    ], string='Shirt Open', readonly=True, copy=False)
    shirt_collar = fields.Selection([
        ('Simple Collar', 'Simple Collar'),
        ('Chinese Collar', 'Chinese Collar')
    ], string='Shirt Collar', copy=False)
    shirt_pocket = fields.Selection([
        ('No Pocket', 'No Pocket'),
        ('Single Pocket', 'Single Pocket'),
        ('Double Pocket', 'Double Pocket'),
    ], string='Shirt Pocket', copy=False)
    shirt_shoulder_type = fields.Selection([
        ('Shoulder', 'Shoulder'),
        ('No Shoulder', 'No Shoulder'),
    ], string='Shirt Shoulder', copy=False)
    shirt_patti = fields.Selection([
        ('Baay Patti', 'Baay Patti'),
        ('No Patti', 'No Patti'),
    ], string='Shirt Patti', copy=False)
    shirt_bombay_patti = fields.Boolean(string="Shirt Bombay Patti")
    shirt_fancy_button = fields.Float(string="Shirt Fancy Button")
    shirt_note = fields.Text(string="Shirt Note")
    shirt_design_no = fields.Char(string="Shirt Design no")
    shirt_half_sleeve1 = fields.Char()
    shirt_collar_shirt = fields.Char()

    # Pent map
    pent_length = fields.Char(string="Pent Length")
    pent_kamar = fields.Char(string="Pent Kamar")
    pent_seat = fields.Char(string="Pent Seat")
    pent_jang = fields.Char(string="Pent Jang")
    pent_ghutan = fields.Char(string="Pent Ghutan")
    pent_gothan = fields.Char(string="Pent Gothan")
    pent_moli = fields.Char(string="Pent Moli")
    pent_jolo = fields.Char(string="Pent Jolo")
    pent_thigh = fields.Char(string="Pent Thigh")
    pent_chipti = fields.Selection([
        ('No Chipti', 'No Chipti'),
        ('V Chipti', 'V Chipti'),
        ('2 Chipti', '2 Chipti'),
    ], string='Pent Chipti', copy=False)
    pent_belt = fields.Selection([
        ('Long', 'Long'),
        ('Cutt Belt', 'Cutt Belt'),
    ], string="બેલ્ટ(Belt)", copy=False)
    pent_greep = fields.Boolean('Greep')
    pent_pocket = fields.Selection([
        ('Side Pocket', 'Side Pocket'),
        ('Cross Pocket', 'Cross Pocket'),
    ], string='Pocket', copy=False, default='Side Pocket')
    pent_back_pocket = fields.Selection([
        ('Single Pocket', 'Single Pocket'),
        ('Double Pocket', 'Double Pocket'),
    ], string="Back Pocket", copy=False, default="Single Pocket")
    pent_chirel_pocket = fields.Boolean(string="Pent Chirel Pocket")
    pent_low_waist = fields.Boolean(string="લો વેસ્ટ(Low Waist)")
    pent_gaaz = fields.Boolean(string="ગાઝ(Gaaz)")
    pent_mobile_pocket = fields.Boolean(string="Pent Mobile Pocket")
    pent_watch_pocket = fields.Boolean(string="Pent 2 Watch Pocket")
    pent_khicchi = fields.Boolean(string="Pent Khichchi")
    pent_note = fields.Text(string="Pent Note")
    pent_design_no = fields.Char(string="Pent Design no")
    pent_a = fields.Char(string="A")
    pent_b = fields.Char(string="B")
    pent_c = fields.Char(string="C")
    pent_d = fields.Char(string="D")

    # Pathani map
    pathani_length = fields.Char(string="લંબાઈ(Length)")
    pathani_shoulder = fields.Char(string="સોલ્ડર(Shoulder)")
    pathani_sleeve_length = fields.Char(string="બાય(Sleeve)")
    pathani_sleeve_length1 = fields.Char()
    pathani_sleeve_length2 = fields.Char()
    pathani_chest = fields.Char(string="છાતી(Chest)")
    pathani_pet = fields.Char(string="પેચ(Pech)")
    pathani_cuff = fields.Char(string="કફ(Cuff)")
    pathani_seat = fields.Char(string="સીટ(Seat)")
    pathani_half_sleeve = fields.Char()
    pathani_half_sleeve_patti = fields.Selection([
        ('Simple', 'Simple'),
        ('Patti', 'Patti')], string="Sleeve Patti", copy=False)
    pathani_petch = fields.Char(string="Petch")
    pathani_petch1 = fields.Char()
    pathani_petch2 = fields.Char()
    pathani_open_shirt = fields.Selection([
        ('Open', 'Open'),
        ('Bushirt', 'Bushirt')
    ], string='Open', readonly=True, copy=False)
    pathani_collar = fields.Selection([
        ('Simple Collar', 'Simple Collar'),
        ('Chinese Collar', 'Chinese Collar')
    ], string='Collar', copy=False)
    pathani_pocket = fields.Selection([
        ('No Pocket', 'No Pocket'),
        ('Single Pocket', 'Single Pocket'),
        ('Double Pocket', 'Double Pocket'),
    ], string='Pocket', copy=False)
    pathani_shoulder_type = fields.Selection([
        ('Shoulder', 'Shoulder'),
        ('No Shoulder', 'No Shoulder'),
    ], string='Shoulder', copy=False)
    pathani_patti = fields.Selection([
        ('Baay Patti', 'Baay Patti'),
        ('No Patti', 'No Patti'),
    ], string='Patti', copy=False)
    pathani_bombay_patti = fields.Boolean(string="Bombay Patti")
    pathani_note = fields.Text(string="Note")
    pathani_design_no = fields.Char(string="Design no")
    pathani_fancy_button = fields.Float(string="Fancy Button")
    pathani_half_sleeve1 = fields.Char()
    pathani_collar_pathani = fields.Char()

    # Lengho map
    lengho_length = fields.Char(string="Lengho Length")
    lengho_kamar = fields.Char(string="Lengho Kamar")
    lengho_seat = fields.Char(string="Lengho Seat")
    lengho_jang = fields.Char(string="Lengho Jang")
    lengho_ghutan = fields.Char(string="Lengho Ghutan")
    lengho_gothan = fields.Char(string="Lengho Gothan")
    lengho_moli = fields.Char(string="Lengho Moli")
    lengho_jolo = fields.Char(string="Lengho Jolo")
    lengho_thigh = fields.Char(string="Lengho Thigh")
    lengho_chipti = fields.Selection([
        ('No Chipti', 'No Chipti'),
        ('V Chipti', 'V Chipti'),
        ('2 Chipti', '2 Chipti'),
    ], string='Chipti', copy=False)
    lengho_belt = fields.Selection([
        ('Long', 'Long'),
        ('Cutt Belt', 'Cutt Belt'),
    ], string='Belt', copy=False)
    lengho_greep = fields.Boolean('Greep')
    lengho_pocket = fields.Selection([
        ('Side Pocket', 'Side Pocket'),
        ('Cross Pocket', 'Cross Pocket'),
    ], string='Pocket', copy=False, default='Side Pocket')
    lengho_back_pocket = fields.Selection([
        ('Single Pocket', 'Single Pocket'),
        ('Double Pocket', 'Double Pocket'),
    ], string="Back Pocket", copy=False, default="Single Pocket")
    lengho_chirel_pocket = fields.Boolean(string="Chirel Pocket")
    lengho_low_waist = fields.Boolean(string="Low Waist")
    lengho_gaaz = fields.Boolean(string="Gaaz")
    lengho_mobile_pocket = fields.Boolean(string="Mobile Pocket")
    lengho_watch_pocket = fields.Boolean(string="2 Watch Pocket")
    lengho_khicchi = fields.Boolean(string="Khichchi")
    lengho_note = fields.Text(string="Note")
    lengho_design_no = fields.Char(string="Design no")

    # Kurto map
    kurto_length = fields.Char(string="Kurto Length")
    kurto_shoulder = fields.Char(string="Kurto Shoulder")
    kurto_sleeve_length = fields.Char(string="Kurto Sleeve Length")
    kurto_sleeve_length1 = fields.Char()
    kurto_sleeve_length2 = fields.Char()
    kurto_chest = fields.Char(string="Kurto Chest")
    kurto_pet = fields.Char(string="Kurto Pet")
    kurto_cuff = fields.Char(string="Kurto Cuff")
    kurto_seat = fields.Char(string="Kurto Seat")
    kurto_half_sleeve = fields.Char()
    kurto_half_sleeve_patti = fields.Selection([
        ('Simple', 'Simple'),
        ('Patti', 'Patti')], string="Sleeve Patti", copy=False)
    kurto_petch = fields.Char(string="Petch")
    kurto_petch1 = fields.Char()
    kurto_petch2 = fields.Char()
    kurto_open_shirt = fields.Selection([
        ('Open', 'Open'),
        ('Bushirt', 'Bushirt')
    ], string='Open', readonly=True, copy=False)
    kurto_collar = fields.Selection([
        ('Simple Collar', 'Simple Collar'),
        ('Chinese Collar', 'Chinese Collar')
    ], string='Collar', copy=False)
    kurto_pocket = fields.Selection([
        ('No Pocket', 'No Pocket'),
        ('Single Pocket', 'Single Pocket'),
        ('Double Pocket', 'Double Pocket'),
    ], string='Pocket', copy=False)
    kurto_shoulder_type = fields.Selection([
        ('Shoulder', 'Shoulder'),
        ('No Shoulder', 'No Shoulder'),
    ], string='Shoulder', copy=False)
    kurto_patti = fields.Selection([
        ('Baay Patti', 'Baay Patti'),
        ('No Patti', 'No Patti'),
    ], string='Patti', copy=False)
    kurto_bombay_patti = fields.Boolean(string="Bombay Patti")
    kurto_note = fields.Text(string="Note")
    kurto_fancy_button = fields.Float(string="Fancy Button")
    kurto_design_no = fields.Char(string="Design no")
    kurto_half_sleeve1 = fields.Char()
    kurto_collar_kurto = fields.Char()

    # Chorni map
    chorni_length = fields.Char(string="Chorni Length")
    chorni_kamar = fields.Char(string="Chorni Kamar")
    chorni_seat = fields.Char(string="Chorni Seat")
    chorni_jang = fields.Char(string="Chorni Jang")
    chorni_ghutan = fields.Char(string="Chorni Ghutan")
    chorni_gothan = fields.Char(string="Chorni Gothan")
    chorni_moli = fields.Char(string="Chorni Moli")
    chorni_jolo = fields.Char(string="Chorni Jolo")
    chorni_thigh = fields.Char(string="Chorni Thigh")
    chorni_chipti = fields.Selection([
        ('No Chipti', 'No Chipti'),
        ('V Chipti', 'V Chipti'),
        ('2 Chipti', '2 Chipti'),
    ], string='Chipti', copy=False)
    chorni_belt = fields.Selection([
        ('Long', 'Long'),
        ('Cutt Belt', 'Cutt Belt'),
    ], string='Belt', copy=False)
    chorni_greep = fields.Boolean('Greep')
    chorni_pocket = fields.Selection([
        ('Side Pocket', 'Side Pocket'),
        ('Cross Pocket', 'Cross Pocket'),
    ], string='Pocket', copy=False, default='Side Pocket')
    chorni_back_pocket = fields.Selection([
        ('Single Pocket', 'Single Pocket'),
        ('Double Pocket', 'Double Pocket'),
    ], string="Back Pocket", copy=False, default="Single Pocket")
    chorni_chirel_pocket = fields.Boolean(string="Chirel Pocket")
    chorni_low_waist = fields.Boolean(string="Low Waist")
    chorni_gaaz = fields.Boolean(string="Gaaz")
    chorni_mobile_pocket = fields.Boolean(string="Mobile Pocket")
    chorni_watch_pocket = fields.Boolean(string="2 Watch Pocket")
    chorni_khicchi = fields.Boolean(string="Khichchi")
    chorni_note = fields.Text(string="Note")
    chorni_design_no = fields.Char(string="Design no")

    # Coti map
    coti_length = fields.Char(string="Coti Length")
    coti_shoulder = fields.Char(string="Coti Shoulder")
    coti_sleeve_length = fields.Char(string="Coti Sleeve Length")
    coti_sleeve_length1 = fields.Char()
    coti_sleeve_length2 = fields.Char()
    coti_chest = fields.Char(string="Coti Chest")
    coti_half_sleeve = fields.Char()
    coti_half_sleeve_patti = fields.Selection([
        ('Simple', 'Simple'),
        ('Patti', 'Patti')], string="Sleeve Patti", copy=False)
    coti_petch = fields.Char(string="Petch")
    coti_petch1 = fields.Char()
    coti_petch2 = fields.Char()
    coti_pet = fields.Char(string="Coti Pet")
    coti_cuff = fields.Char(string="Coti Cuff")
    coti_seat = fields.Char(string="Coti Seat")
    coti_open_shirt = fields.Selection([
        ('Open', 'Open'),
        ('Bushirt', 'Bushirt')
    ], string='Coti Open', readonly=True, copy=False)
    coti_collar = fields.Selection([
        ('Simple Collar', 'Simple Collar'),
        ('Chinese Collar', 'Chinese Collar')
    ], string='Coti Collar', copy=False)
    coti_pocket = fields.Selection([
        ('No Pocket', 'No Pocket'),
        ('Single Pocket', 'Single Pocket'),
        ('Double Pocket', 'Double Pocket'),
    ], string='Coti Pocket', copy=False)
    coti_shoulder_type = fields.Selection([
        ('Shoulder', 'Shoulder'),
        ('No Shoulder', 'No Shoulder'),
    ], string='Coti Shoulder', copy=False)
    coti_patti = fields.Selection([
        ('Baay Patti', 'Baay Patti'),
        ('No Patti', 'No Patti'),
    ], string='Coti Patti', copy=False)
    coti_bombay_patti = fields.Boolean(string="Coti Bombay Patti")
    coti_fancy_button = fields.Float(string="Coti Fancy Button")
    coti_note = fields.Text(string="Coti Note")
    coti_design_no = fields.Char(string="Coti Design no")
    coti_half_sleeve1 = fields.Char()
    coti_collar_coti = fields.Char()

    # Blazer map
    blazer_length = fields.Char(string="Blazer Length")
    blazer_shoulder = fields.Char(string="Blazer Shoulder")
    blazer_sleeve_length = fields.Char(string="Blazer Sleeve Length")
    blazer_sleeve_length1 = fields.Char()
    blazer_sleeve_length2 = fields.Char()
    blazer_chest = fields.Char(string="Blazer Chest")
    blazer_half_sleeve = fields.Char()
    blazer_half_sleeve_patti = fields.Selection([
        ('Simple', 'Simple'),
        ('Patti', 'Patti')], string="Sleeve Patti", copy=False)
    blazer_petch = fields.Char(string="Petch")
    blazer_petch1 = fields.Char()
    blazer_petch2 = fields.Char()
    blazer_pet = fields.Char(string="Blazer Pet")
    blazer_cuff = fields.Char(string="Blazer Cuff")
    blazer_seat = fields.Char(string="Blazer Seat")
    blazer_open_shirt = fields.Selection([
        ('Open', 'Open'),
        ('Bushirt', 'Bushirt')
    ], string='Blazer Open', readonly=True, copy=False)
    blazer_collar = fields.Selection([
        ('Simple Collar', 'Simple Collar'),
        ('Chinese Collar', 'Chinese Collar')
    ], string='Blazer Collar', copy=False)
    blazer_pocket = fields.Selection([
        ('No Pocket', 'No Pocket'),
        ('Single Pocket', 'Single Pocket'),
        ('Double Pocket', 'Double Pocket'),
    ], string='Blazer Pocket', copy=False)
    blazer_shoulder_type = fields.Selection([
        ('Shoulder', 'Shoulder'),
        ('No Shoulder', 'No Shoulder'),
    ], string='Blazer Shoulder', copy=False)
    blazer_patti = fields.Selection([
        ('Baay Patti', 'Baay Patti'),
        ('No Patti', 'No Patti'),
    ], string='Blazer Patti', copy=False)
    blazer_bombay_patti = fields.Boolean(string="Blazer Bombay Patti")
    blazer_fancy_button = fields.Float(string="Blazer Fancy Button")
    blazer_note = fields.Text(string="Blazer Note")
    blazer_design_no = fields.Char(string="Blazer Design no")
    blazer_half_sleeve1 = fields.Char()
    blazer_collar_blazer = fields.Char()
