"""
数据库使用路由配置
"""


class MyDBRouter:

    route_app_labels = {'polls'}

    def db_for_read(self, model, **hints):
        """
        建议用于读取“模型”类型对象的数据库。
        :param model: 模块信息
        :param hints: 其它可使用的附加信息
        :return:
        """
        if model._meta.app_label in self.route_app_labels:
            return 'db1'
        return None

    def db_for_write(self, model, **hints):
        """
        建议用于写“模型”类型对象的数据库。
        """
        if model._meta.app_label in self.route_app_labels:
            return 'db1'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        如果允许 obj1 和 obj2 之间的关系，返回 True 。如果阻止关系，返回 False ，
        或如果路由没意见，则返回 None。这纯粹是一种验证操作，由外键和多对多操作决定是否应该允许关系。
        如果没有路由有意见（比如所有路由返回 None），则只允许同一个数据库内的关系。
        """
        if (
                obj1._meta.app_label in self.route_app_labels or
                obj2._meta.app_label in self.route_app_labels
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        决定是否允许迁移操作在别名为 db 的数据库上运行。
        如果操作运行，那么返回 True ，如果没有运行则返回 False ，或路由没有意见则返回 None 。
        """
        if app_label in self.route_app_labels:
            return db == 'db1'
        return None
