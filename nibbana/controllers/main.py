import logging
from odoo import http, _
from odoo import tools
from werkzeug.utils import redirect

logger = logging.getLogger(__name__)


class NibbanaController(http.Controller):
    @http.route('/nibbana/create_default_areas', auth='user')
    def create_default_areas(self):
        """
        current_areas = http.request.env['nibbana.area'].search([
                                        ('create_uid', '=', http.request.uid)])
        if current_areas:
            # Areas already exist
            logger.info('User ID {} already has areas. Not creating.'.format(
                                                        http.request.uid))
        else:
        """
        http.request.env['nibbana.area'].create({
            'name': 'Business',
            'color': '#ACE7FF',
            'description': _('My work projects and tasks')
        })
        http.request.env['nibbana.area'].create({
            'name': 'Family',
            'color': '#FFCBC1',
            'description': _('Kids, wife, parents, home')
        })
        http.request.env['nibbana.area'].create({
            'name': 'Entertainment',
            'color': '#FCC2FF',
            'description': _('Fun, excitements, cinema, travel etc')
        })
        http.request.env['nibbana.area'].create({
            'name': 'Health',
            'color': '#FFABAB',
            'description': _('Health, fitness')
        })
        http.request.env['nibbana.area'].create({
            'name': 'Social',
            'color': '#BFFCC6',
            'description': _('Help to my friends and my contribution to the world')
        })
        http.request.env['nibbana.area'].create({
            'name': 'Studies',
            'color': '#ECD4FF',
            'description': _('My carrier and personal growth')
        })
        http.request.env['nibbana.area'].create({
            'name': 'Spiritual',
            'color': '#FFFFD1',
            'description': _('My activities related to connection to the Great Spirit')
        })
        action_id = http.request.env.ref('nibbana.area_action').id
        menu_id = http.request.env.ref('nibbana.area_menu').id
        return redirect(
            '/web#view_type=list&model=nibbana.area&menu_id={}&action={}'.format(
                                                            menu_id, action_id))


    @http.route('/nibbana/create_default_contexts', auth='user')
    def create_default_contexts(self):
        """
        current_contexts = http.request.env['nibbana.context'].search([
                                        ('create_uid', '=', http.request.uid)])
        if current_contexts:
            # Areas already exist
            logger.info('User ID {} already has contexts. Not creating.'.format(
                                                        http.request.uid))
        else:
        """
        http.request.env['nibbana.context'].create({
            'name': 'Call',
            'description': _('When I have the opportunity to place calls')
        })
        http.request.env['nibbana.context'].create({
            'name': 'City',
            'description': _('When I am in the city')
        })
        http.request.env['nibbana.context'].create({
            'name': 'Buy',
            'description': _('When I can do shopping')
        })
        http.request.env['nibbana.context'].create({
            'name': 'Home',
            'description': _('Whan I am at home')
        })
        http.request.env['nibbana.context'].create({
            'name': 'Office',
            'description': _('When I am in the office')
        })
        http.request.env['nibbana.context'].create({
            'name': 'PC',
            'description': _('When I use my personal computer')
        })
        http.request.env['nibbana.context'].create({
            'name': 'Mobile',
            'description': _('Work I can do on mobile internet')
        })
        http.request.env['nibbana.context'].create({
            'name': 'Driving',
            'description': _('Tasks I can complete while driving somewhere')
        })
        http.request.env['nibbana.context'].create({
            'name': 'Meeting',
            'description': _('Issues I can solve on the meeting')
        })
        http.request.env['nibbana.context'].create({
            'name': 'Walking',
            'description': _('Things I can do on a walk')
        })
        http.request.env['nibbana.context'].create({
            'name': 'Read',
            'description': _('Tasks that require reading new information')
        })
        http.request.env['nibbana.context'].create({
            'name': 'Watch',
            'description': _('Tasks that require to watch something')
        })
        http.request.env['nibbana.context'].create({
            'name': 'Listen',
            'description': _('Tasks that require to listen to something')
        })        
        http.request.env['nibbana.context'].create({
            'name': 'Discuss',
            'description': _('Need to discuss')
        })        
        http.request.env['nibbana.context'].create({
            'name': 'Quick',
            'description': _('Little time is required to complete a task')
        })        
        action_id = http.request.env.ref('nibbana.contexts_action').id
        menu_id = http.request.env.ref('nibbana.contexts_menu').id
        return redirect(
            '/web#view_type=list&model=nibbana.context&menu_id={}&action={}'.format(
                                                                menu_id, action_id))


    @http.route('/nibbana/signup', auth='user')
    def signup(self):
        user = http.request.env['res.users'].browse(http.request.uid)
        email = user.partner_id.email
        if not email:
            return http.request.render('nibbana.email_not_set')
        else:
            mail = http.request.env['mail.mail'].create({
                'subject': 'Nibbana subscribe request',
                'email_from': email,
                'email_to': 'odooist@gmail.com',
                'body_html': '<p>Email: {}</p>'.format(email),
                'body': 'Email: {}'.format(email),
            })
            mail.send()
            return http.request.render('nibbana.email_sent', 
                                       qcontext={'email': email})
