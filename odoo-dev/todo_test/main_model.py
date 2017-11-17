#-*- coding: UTF-8 -*-
from openerp import models, fields, api
import logging

class Qingjd(models.Model):
    _name = 'qingjia.qingjd'
    name = fields.Char(string="申请人", required=True)
    manager = fields.Char(string="主管", required=True)
    is_company = fields.Boolean(String="选择",defaults=False)
    emp_mgr = fields.Selection(selection=[('personal', '个人'), ('company', '集体')],
                               default='personal')
    beginning = fields.Datetime(string="开始时间", required=True, default=fields.Datetime.now())
    ending = fields.Datetime(string="结束时间", required=True)
    reason = fields.Text(string="请假事由", required=True)
    accept_reason = fields.Text(string="同意理由",default="同意。")
    image = fields.Binary('Image')
    message = fields.Char(hint='公司')
    parent_id = fields.Many2one('res.partner')
    active = fields.Boolean(string='Active')
    color = fields.Integer('Color Index')

    #compute 没有写入数据库 on the fly 可以被workflow的condition调用
    current_name = fields.Many2one('res.users', string="当前登录人",compute="_get_current_name")
    is_manager = fields.Boolean(compute='_get_is_manager')
    state = fields.Selection([('draft', "草稿"),
                              ('confirmed', '待审核'),
                              ('accepted', '批准'),
                              ('rejected', '拒绝'),],
                             string='状态',default='draft',readonly=True)

    #使用新的api
    @api.model
    def _get_default_name(self):
        uid = self.env.uid
        res = self.env['res.users'].search([('user_id','=',uid)])
        name = res.name
        return name
    _defaults = {'name': _get_default_name}

    def _get_is_manager(self):
                self.is_manager = True

    def _get_current_name(self):
        name = self.env.name
        self.current_name = name

    def draft(self, cr, uid, ids, context=None):
        if context is None:context={}
        self.write(cr,uid,ids,{'state':'draft'},context=context)
        return True
    def confirm(self, cr, uid, ids, context=None):
        if context is None:context={}
        self.write(cr,uid,ids,{'state':'confirmed'},context=context)
        return True
    def accept(self, cr, uid, ids, context=None):
        if context is None:context={}
        self.write(cr,uid,ids,{'state':'accepted'},context=context)
        print('你的请假单被批准了')
        return True
    def reject(self, cr, uid, ids, context=None):
        if context is None:context={}
        self.write(cr,uid,ids,{'state':'rejected'},context=context)
        print('抱歉，你的请假单没有被批准。')
        return True

    @api.onchange('emp_mgr')
    def on_change_emp_mgr(self):
        print('===============================')
        print('emp_mgr:  '+ self.emp_mgr)
        if self.emp_mgr == 'company':
            self.is_company = True
        if self.emp_mgr == 'personal':
            self.is_company = False



