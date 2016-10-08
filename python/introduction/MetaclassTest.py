#!/usr/bin/python
# -*- coding: utf-8 -*-

class Field(object):
    def __init__(self, name, column_type):
        self.name = name
        self.column_type = column_type
    def __str__(self):
        return '<%s======%s>' % (self.__class__.__name__, self.name)

class StringField(Field):
    def __init__(self, name):
        super(StringField, self).__init__(name, 'varchar(100)')

class IntegerField(Field):
    def __init__(self, name):
        super(IntegerField, self).__init__(name, 'bigint')

class ModelMetaclass(type):
    def __new__(cls, name, bases, attrs):
        if name=='Model':
            return type.__new__(cls, name, bases, attrs)
        print(name)
        print(bases)
        print attrs
        mappings = dict()
        for k, v in attrs.iteritems():
            print('����ɶ: ��%s��  ==>  ��%s��' % (k, v))
            if isinstance(v, Field):
                print('Found mapping: %s==>%s' % (k, v))
                mappings[k] = v
        for k in mappings.iterkeys():
            attrs.pop(k)
        attrs['__table__'] = name # �������������һ��
        attrs['__mappings__'] = mappings # �������Ժ��е�ӳ���ϵ
        print attrs
        return type.__new__(cls, name, bases, attrs)

class Model(dict):
    __metaclass__ = ModelMetaclass

    def __init__(self, **kw):
        super(Model, self).__init__(**kw)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Model' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        print "ʲô��"
        self[key] = value

    def save(self):
        fields = []
        params = []
        args = []
        for k, v in self.__mappings__.iteritems():
            print "adsafasdfa====================="+k
            fields.append(v.name)
            params.append('?')
            args.append(getattr(self, k, None))
        sql = 'insert into %s (%s) values (%s)' % (self.__table__, ','.join(fields), ','.join(params))
        print('SQL: %s' % sql)
        print('ARGS: %s' % str(args))

class User(Model):
    # ����������Ե��е�ӳ�䣺
    id = IntegerField('id')
    name = StringField('username')
    email = StringField('email')
    password = StringField('password')
    def Hello (self):
        pass

# ����һ��ʵ����
u = User(id=12345, name='Michael', email='test@orm.org', password='my-pwd')
# ���浽���ݿ⣺
u.save()
