from app import app, db
from flask_admin import Admin, BaseView, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from app.models import Category, Product, UserRole, Receipt, ReceiptDetail
from flask_login import current_user, logout_user
from flask import redirect, request, jsonify, flash
import utils
from datetime import datetime
from markupsafe import Markup


class AuthenticatedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role.__eq__(UserRole.ADMIN)

class ProductView(AuthenticatedModelView):
    can_delete = True
    column_searchable_list = ['name', 'description']
    column_filters = ['name', 'price']
    column_exclude_list = ['image', 'create_date']
    column_sortable_list = ['name', 'price', 'quantity']
    column_labels = {
        'name': 'Tên',
        'description': 'Mô tả',
        'price': 'Giá',
        'quantity': 'Số lượng',
        'category': 'Danh mục'
    }

    def quantity_warning(view, context, model, name):
        if model.quantity < 5:
            return Markup(f'<span class="text-danger font-weight-bold">{model.quantity} (Sắp hết!)</span>')
        return model.quantity

    column_formatters = {
        'quantity': quantity_warning
    }

class CreateReceiptView(BaseView):
    @expose('/')
    def index(self):
        products = Product.query.filter(Product.active == True).all()
        return self.render('admin/create_receipt.html', products=products)

    @expose('/save', methods=['POST'])
    def save(self):
        data = request.json
        items = data.get('items')

        if not items:
            return jsonify({'code': 400, 'msg': 'Chưa chọn món nào!'})

        try:
            receipt = Receipt(user_id=current_user.id, created_date=datetime.now())
            db.session.add(receipt)
            db.session.commit()

            for item in items:
                detail = ReceiptDetail(
                    receipt_id=receipt.id,
                    product_id=int(item['id']),
                    quantity=int(item['quantity']),
                    unit_price=float(item['price'])
                )
                db.session.add(detail)

            db.session.commit()
            return jsonify({'code': 200, 'msg': 'Lập hóa đơn thành công!'})
        except Exception as ex:
            return jsonify({'code': 500, 'msg': str(ex)})

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN

class ReceiptView(AuthenticatedModelView):
    column_display_pk = True
    can_create = False
    can_edit = False
    can_delete = True
    can_export = True
    can_view_details = True

    column_list = ['id', 'user', 'created_date', 'product_count', 'total_amount']

    column_labels = {
        'id': 'Mã hóa đơn',
        'user': 'Người lập/Khách',
        'created_date': 'Ngày lập',
        'product_count': 'Số lượng món',
        'total_amount': 'Tổng tiền (VNĐ)',
        'details': 'Chi tiết sản phẩm'
    }

    column_filters = ['created_date', 'user.name']

    def _format_money(view, context, model, name):
        total = sum(d.quantity * d.unit_price for d in model.details)
        final_total = total + (total * 0.05)
        return "{:,.0f}".format(final_total)

    #Đếm món
    def _format_count(view, context, model, name):
        return len(model.details)

    def _format_date(view, context, model, name):
        if model.created_date:
            return model.created_date.strftime('%d/%m/%Y %H:%M:%S')
        return ""

    column_formatters = {
        'total_amount': _format_money,
        'product_count': _format_count,
        'created_date': _format_date
    }

class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')

    def is_accessible(self):
        return current_user.is_authenticated

class MyAdminIndex(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html', stats=utils.category_stats())

class StatsView(BaseView):
    @expose('/')
    def index(self):
        kw = request.args.get('kw')
        from_date = request.args.get('from_date')
        to_date = request.args.get('to_date')
        year = request.args.get('year', datetime.now().year)

        return self.render('admin/stats.html',
                           month_stats=utils.product_month_stats(year=year),
                           stats=utils.product_stats(kw=kw, from_date=from_date, to_date=to_date))

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN

admin = Admin(app=app,name="D-coffee Administration", index_view=MyAdminIndex())

admin.add_view(AuthenticatedModelView(Category, db.session))
admin.add_view(ProductView(Product, db.session))
admin.add_view(StatsView(name='Stats'))
admin.add_view(LogoutView(name='Logout'))
admin.add_view(CreateReceiptView(name='Lập Hóa Đơn', endpoint='create-receipt'))
admin.add_view(ReceiptView(Receipt, db.session, name='Quản lý Hóa đơn'))