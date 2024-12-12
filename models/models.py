# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class esdeveniments(models.Model):
    _name = 'esdeveniments.esdeveniments'
    _description = 'esdeveniments.esdeveniments'

    nom = fields.Char(string="Nom", required=True)
    tipo = fields.Selection(selection=[('1', '1'),('2', '2'),('3', '3'),('4', '4'),('5', '5')], string="Tipo", required=True)
    data_inici = fields.Datetime(string="Data de Inici")
    data_fi = fields.Datetime(string="Data de Fi")
    lloc = fields.Char(string="Lloc")
    descripcio = fields.Char(string="Descripcio")
    imatge = fields.Image(string="Foto", max_width=200)
    llista_participants = fields.Many2many("esdeveniments.participants", string="Participants")

    @api.constrains('data_inici', 'data_fi')
    def _check_dates(self):
        for record in self:
            if record.data_inici and record.data_fi:
                if record.data_inici > record.data_fi:
                    raise ValidationError("La data d'inici no pot ser posterior a la data de fi.")

    @api.constrains('llista_participants')
    def _check_participantes(self):
        for record in self:
            if record.llista_participants:
                if len(record.llista_participants) > 1:
                    raise ValidationError("No pot haver-hi més de 1 participant.")


class participants(models.Model):
    _name = 'esdeveniments.participants'
    _description = 'esdeveniments.participants'

    nom = fields.Char(string="Nom", required=True)
    cognoms = fields.Char(string="Cognoms", required=True)
    dni = fields.Char(string="Dni", required=True)
    diners = fields.Integer(string="Diners", compute="_compute_diners", store=True)
    llista_esdeveniments = fields.Many2many("esdeveniments.esdeveniments", string="Esdeveniments")

    @api.depends('llista_esdeveniments')
    def _compute_diners(self):
        for record in self:
            record.diners = len(record.llista_esdeveniments) * 1000