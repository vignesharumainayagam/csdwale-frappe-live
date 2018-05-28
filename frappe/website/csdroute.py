from __future__ import unicode_literals
import frappe, os

from frappe.website.utils import can_cache, delete_page_cache, extract_title
from frappe.model.document import get_controller
from six import text_type
import io


class CustomURL(object):
    def __init__(self):
        self.IsCustom = None

    def getCustomUrl(self):
        return self.custom_url

    def setCustomPage(self,page):
            self.IsCustom = True  
            self.custom_url =  page


    def setCustomUrl(self,path):

        self.url=path.split('/')[0].lower()
        self.url_length =len(path.split('/'))

        
        if(self.url_length == 1):
            self.getsingledata(path)

        if(self.url_length == 2):
            self.gettwodata(path) 

        if(self.url_length == 3):
            self.getthirddata(path)

        if(self.url_length == 4):
            self.getfourdata(path)

        if(self.url_length == 5):
            self.getfivedata(path)    


    def getsingledata(self,path):
        self.routes = self.check_routes(path,['Custom Page','Category'])

        # custom pages
        if(self.routes.get('doctype') == 'Custom Page' and self.routes.get("route") == path ):
            self.setCustomPage('custompage')

        # csd-cars
        path = path.replace('csd-', '')
        if path.split('/')[0]:
            self.Category = self.check_routes(path.split('/')[0],['Category'])
            if(self.Category.get('doctype') == 'Category' and self.Category.get("route") == path.split('/')[0]):
                self.setCustomPage('cathomepage')

        # csd-dealers
        if path.split('/')[0]:
            self.Category = self.check_routes(path.split('/')[0],['Category'])
            if(path.split('/')[0] == "dealers" ):
                self.setCustomPage('dealercity')

    def gettwodata(self,path):
        dealerpath = path.split('/')
        self.routes = self.check_routes(dealerpath[1],['News'])

        #news/news1
        if(self.routes.get('doctype') == 'News' and dealerpath[0] == 'news' and self.routes.get("route") == dealerpath[1] ):
            self.setCustomPage('blog_detail')

        #csd-cars/honda
        path = path.replace('csd-', '') 
        if path.split('/')[0]:
            self.ItemBrand = self.check_routes(path.split('/')[1],['ItemBrand'])
            self.Category = self.check_routes(path.split('/')[0],['Category'])

            if( self.Category.get('doctype') == 'Category' and self.Category.get("route") == path.split('/')[0] 
                and self.ItemBrand.get('doctype') == 'ItemBrand' 
                and self.ItemBrand.get("route") == path.split('/')[1]):
                self.setCustomPage('listpage')  

        #csd-dealers/chennai 
        if path.split('/')[0]:
            self.City = self.check_routes(path.split('/')[1],['City'])

            if( "dealers" == path.split('/')[0] 
                and self.City.get('doctype') == 'City' 
                and self.City.get("route") == path.split('/')[1] ):
                self.setCustomPage('dealercategory')  

    def getthirddata(self,path):

        #csd-cars/honda/brio 
        path = path.replace('csd-', '')
        if path.split('/')[0]:
            self.ItemBrand = self.check_routes(path.split('/')[1],['ItemBrand'])
            self.Category = self.check_routes(path.split('/')[0],['Category'])
            self.Item = self.check_routes(path.split('/')[2],['Item'])

            if( self.Category.get('doctype') == 'Category' and self.Category.get("route") == path.split('/')[0] 
                and self.ItemBrand.get('doctype') == 'ItemBrand' 
                and self.ItemBrand.get("route") == path.split('/')[1] 
                and self.Item.get('doctype') == 'Item' 
                and self.Item.get("route") == path.split('/')[2] ):
                self.setCustomPage('detailpage') 

        #csd-dealers/chennai/cars 
        if path.split('/')[0]:
            self.City = self.check_routes(path.split('/')[1],['City'])
            self.Category = self.check_routes(path.split('/')[2],['Category'])

            if( "dealers" == path.split('/')[0]  
                and self.City.get('doctype') == 'City' 
                and self.City.get("route") == path.split('/')[1] 
                and self.Category.get('doctype') == 'Category' 
                and self.Category.get("route") == path.split('/')[2] ):

                self.setCustomPage('dealerbrand') 


    def getfourdata(self,path):

        #csd-cars/honda/brio/images 
        path = path.replace('csd-', '')
        if "-price" in path:
            path = path.replace('-price', '')

        if path.split('/')[0]:
            self.ItemBrand = self.check_routes(path.split('/')[1],['ItemBrand'])
            self.Category = self.check_routes(path.split('/')[0],['Category'])
            self.Item = self.check_routes(path.split('/')[2],['Item'])

            if( self.Category.get('doctype') == 'Category' and self.Category.get("route") == path.split('/')[0] 
                and self.ItemBrand.get('doctype') == 'ItemBrand' 
                and self.ItemBrand.get("route") == path.split('/')[1] 
                and self.Item.get('doctype') == 'Item' 
                and self.Item.get("route") == path.split('/')[2] 
                and "images" == path.split('/')[3]):
                self.setCustomPage('view_images')

        #csd-cars/honda/brio/lxi-price 
        if path.split('/')[0]:
            self.ItemBrand = self.check_routes(path.split('/')[1],['ItemBrand'])
            self.Category = self.check_routes(path.split('/')[0],['Category'])
            self.Item = self.check_routes(path.split('/')[2],['Item'])
            self.Itemvariant = self.check_routes(path.split('/')[3],['Item Variant'])

            if path.split('/')[3]:
                if( self.Category.get('doctype') == 'Category' and self.Category.get("route") == path.split('/')[0] 
                    and self.ItemBrand.get('doctype') == 'ItemBrand' 
                    and self.ItemBrand.get("route") == path.split('/')[1] 
                    and self.Item.get('doctype') == 'Item' 
                    and self.Item.get("route") == path.split('/')[2] 
                    and self.Itemvariant.get('doctype') == 'Item Variant' 
                    and self.Itemvariant.get("route") == path.split('/')[3]):
                    self.setCustomPage('varientdetailpage') 

        #csd-dealers/chennai/cars/honda 
        if path.split('/')[0]:
            self.City = self.check_routes(path.split('/')[1],['City'])
            self.Category = self.check_routes(path.split('/')[2],['Category'])
            self.ItemBrand = self.check_routes(path.split('/')[3],['ItemBrand'])

            if( "dealers" == path.split('/')[0] 
                and self.City.get('doctype') == 'City' 
                and self.City.get("route") == path.split('/')[1] 
                and self.Category.get('doctype') == 'Category' 
                and self.Category.get("route") == path.split('/')[2]
                and self.ItemBrand.get('doctype') == 'ItemBrand' 
                and self.ItemBrand.get("route") == path.split('/')[3] ):

                self.setCustomPage('dealers_list') 

    def getfivedata(self,path):

        #csd-dealers/chennai/cars/honda/contactdealer 
        path = path.replace('csd-', '')
        if path.split('/')[0]:
            self.City = self.check_routes(path.split('/')[1],['City'])
            self.Category = self.check_routes(path.split('/')[2],['Category'])
            self.ItemBrand = self.check_routes(path.split('/')[3],['ItemBrand'])

            if( "dealers" == path.split('/')[0]
                and self.City.get('doctype') == 'City' 
                and self.City.get("route") == path.split('/')[1] 
                and self.Category.get('doctype') == 'Category' 
                and self.Category.get("route") == path.split('/')[2]
                and self.ItemBrand.get('doctype') == 'ItemBrand' 
                and self.ItemBrand.get("route") == path.split('/')[3]
                and "contactdealer" == path.split('/')[4] ):

                self.setCustomPage('homepage')    

    def check_routes(self,path=None,doctypes=None):
        routes = {}
        for doctype in doctypes:
            values = []
            condition = ""
            if path:
                condition += ' {0} `route`=%s limit 1'.format('and' if 'where' in condition else 'where')
                values.append(path)
            try:
                for r in frappe.db.sql("""select route, name from `tab{0}` {1}""".format(doctype,condition), values=values, as_dict=True):
                    routes[r.route] = {"doctype":doctype,"route": r.route}
                    if path:
                        return routes[r.route]
            except Exception as e:
                if e.args[0]!=1054: raise e
        return routes
