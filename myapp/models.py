from ldap3 import Server, Connection, SUBTREE
import re
from flask_login import UserMixin
from myapp.app import db

### LDAP DATA - Get AD User Members of AD Group ###
script_data = 'myapp/ldap-data'
with open(script_data, 'r', encoding='utf-8') as file:
    data = [i.strip() for i in file.readlines()]
    dc_host = data[0]
    domain_root = data[1]
    ad_bind_user = data[2]
    ad_bind_user_pass = data[3]
    ad_users_group = data[4]
ldap_port = 389
server = Server(dc_host, port=ldap_port)
with Connection(server, ad_bind_user, ad_bind_user_pass, auto_bind=True) as conn:
    conn.search(
        search_base=domain_root,
        search_filter='(&(objectClass=GROUP)(cn=' + ad_users_group +'))', 
        search_scope=SUBTREE,
        attributes=['member'], size_limit=0)
    conn_search = list(map(lambda x: x.lower(), conn.entries[0].member.values))
    conn.unbind()
cn_pattern = '^cn=(\w+),'
#########

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True, index=True)
    username = db.Column(db.String(100), index=True)
    is_admin = db.Column(db.String(3), index=True)

    def try_login(username, password):
        '''
        ad_user = ''
        for val in conn_search:
            try:
                re.findall(cn_pattern, val)[0]
                if username == re.findall(cn_pattern, val)[0]:
                    ad_user = val
                    break
            except:
                continue
            
        if not ad_user:
            raise Exception(f'ERROR: {username} not found in {ad_users_group}')
        try:
            with Connection(server, ad_user, password, auto_bind=True) as conn:
                conn.bind()
        except:
            raise Exception('Invalid Creds')
        conn.unbind()
        '''
        return True
    
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

class Wishlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    wishlist = db.Column(db.String(200), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Lottery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    assigned_wishlist = db.Column(db.Integer)