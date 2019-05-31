from lib.render_func import Render
class Hunter(object):

    def __init__(self, target, context):
        self.replace = False
        self.target = target
        self.context = context
        self.nested_dict = False
        self.is_list = False
        self.data_fields = context['data']
        self.hunter_output = dict()
        self.row_count = 0
        
        if 'key' in context['data'] and 'value' in context['data']:
            self.return_all = True
        if 'replace' in context:
            self.replace = True
        if 'nested_dict' in context:
            self.nested_dict = True
            self.target = target[(list(target))[0]][context['nested_dict']]
        if type(target) == list:
            self.is_list = True
            
        self.init_hunt()

    def init_hunt(self):
        for prey in self.target:
            self.tail = None
            self.hunter_output[self.row_count] = dict()
            prey_dict = self.hunter_output[self.row_count]
            prey_dict['self'] = prey
            if self.is_list:
                self.hunt(prey)
                self.row_count += 1 
                continue
            for tail in self.target[prey]:
                if tail in self.data_fields:
                    self.tail = tail
                if type(self.target[prey]) == list:
                    for hair in self.target[prey]:
                        self.hunt(hair)
                    break
                elif type(self.target[prey][tail]) == dict:
                    for hair in self.target[prey][tail]:
                        if tail not in prey_dict:
                            prey_dict[tail] = self.mount_kill(tail, hair)
                        else:
                            prey_dict[tail] += '<br \>'
                            prey_dict[tail] += self.mount_kill(tail, hair)                                                   
                    self.hunt(self.target[prey][tail])
                else:
                    prey_dict[tail] = self.mount_kill(tail, self.target[prey][tail])
            self.row_count += 1    

    def hunt(self, target):
        prey_dict = self.hunter_output[self.row_count]
        for key, value in target.items():
            if self.tail != None:
                prey_dict[self.tail] = key
                self.tail = None
            if type(value) == dict:
                self.hunt(value)
                continue
            if key not in prey_dict:
                prey_dict[key] = self.mount_kill(key, value)
            else:
                prey_dict[key] += '<br \>'
                prey_dict[key] += self.mount_kill(key, value)

    def clean_hunt(self):
        spills = list()
        spoils = dict()
        if 'columns' not in self.context:
            print('You must include columns in actions dict to use Hunter')
            return False
        for column in self.context['columns']:
            spills.append(self.context['columns'][column])
        for dead in self.hunter_output:
            self.trophy = spills
            for key, value in self.hunter_output[dead].items():
                self.trophy = [t.replace(key, str(value)) for t in self.trophy]
                spoils[dead] = self.trophy
        return spoils

    def mount_kill(self, key, value):
        kill = value
        if self.replace == True:
            if str(key) in self.context['replace']:
                context_key = self.context['replace'][key]
                if value in context_key or '*' in context_key:
                    if '*' in context_key:
                        element = context_key['*']["element"]
                        css = context_key['*']["class"]
                        temp_value = context_key['*']["value"]
                        value = temp_value.replace('self', str(value))
                    else:
                        element = context_key[value]["element"]
                        css = context_key[value]["class"]
                        value = context_key[value]["value"]
                    kill = ('<%s class="%s">%s</%s>' % (element, css, value, element))
        if 'render_func' in self.context:
            if key in self.context['render_func']:
                render_func = (self.context['render_func'][key]).replace(str(key), str(value))
                r = Render()
                kill = eval('r.%s' % (render_func))
        return str(kill)
        
        