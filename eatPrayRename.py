import functools
class window_ui():
    def __init__(self):
        self.modular_layout = None
        self.diccionario_try = {} 
        self.ventanaNombre = 'myWindowID'
        self.Titulo = 'eatPrayRename'
        self.Alto = 350
        self.Ancho = 500
        if cmds.window(self.ventanaNombre, exists=True):
            cmds.deleteUI(self.ventanaNombre)
        self.VENTANA = cmds.window(self.ventanaNombre, title='eatPrayRename', width=self.Alto, height = self.Ancho)
   
   
    def select_component(self, component = None, *pArgs):
        cmds.select(component)
    def rename_component(self, ui_list = None, component =None, prefix = None, *pArgs):
        self.new_name = cmds.textField(ui_list[2], q=True, text=True) 
        check_name = cmds.rename(component, '{}{}'.format(self.new_name, prefix))
        
        cmds.button(ui_list[1], label=check_name, edit=True, command= functools.partial(self.select_component, check_name))
        
        if check_name.count('_') == 2:
            cmds.rowColumnLayout(ui_list[0] , edit= True, bgc = [0.1,0.8,0.4])  

    def layout_creator(self, type_element = None, *pArgs):
        if self.modular_layout:
            cmds.deleteUI(self.modular_layout, layout=True)

        self.type_dic = {'skinCluster' : '_skinCluster', 
                        'nurbsSurface' : '_nurbs', 
                        'blendShape' : '_bs', 
                        'parentConstraint' : '_parCon', 
                        'orientConstraint' : '_oriCon', 
                        'pointConstraint' : '_pointCon', 
                        'aimConstraint' : '_aimCon'}
                    
        self.type_list = cmds.ls(type = type_element) 
        self.modular_layout = cmds.rowColumnLayout(numberOfColumns=1, columnOffset=[(1, 'right', 3) ], parent = self.created_layout)
        for element in self.type_list:     
            self.background_color = [0.1,0.8,0.4]
            if element.count('_') != 2:
                self.background_color = [1.0, 0.0, 0.0]
            if type_element == 'skinCluster':
                sentence = 'This Skin is connected to {}'.format(cmds.listConnections('{}.outputGeometry'.format(element))[0])
            elif type_element == 'orientConstraint':   
                sentence = 'This Constraint is connected to {}'.format(cmds.listConnections('{}.constraintRotateX'.format(element))[0])    
            elif type_element == 'pointConstraint':   
                sentence = 'This Constraint is connected to {}'.format(cmds.listConnections('{}.constraintTranslateX'.format(element))[0])        
            elif type_element == 'parentConstraint':   
                sentence = 'This Constraint is connected to {}'.format(cmds.listConnections('{}.constraintTranslateX'.format(element))[0])   
            elif type_element == 'aimConstraint':   
                sentence = 'This Constraint is connected to {}'.format(cmds.listConnections('{}.constraintRotateX'.format(element))[0])                        
            elif type_element == 'blendShape':   
                sentence = 'This BlendShape is connected to {}'.format(cmds.listConnections('{}.constraintRotateX'.format(element))[0])                  
                
            self.generated_layout = cmds.rowColumnLayout('{}_layout'.format(element), numberOfColumns=4, columnOffset = [(1, 'left', 3), (2, 'left', 3), (3, 'left', 0), (4, 'right', 3)], parent = self.modular_layout, ut=True, bgc = self.background_color, w= 700, h=50)    
            self.select_element = cmds.button(label='Select {}'.format(element), command= functools.partial(self.select_component, element), w=175, h=20)
            self.input_name = cmds.textField('{}_ui'.format(element), text=element, w=175, h=20)
            self.pref_subfix = cmds.text(label = self.type_dic.get(type_element), w=175, h=20)
            
            ui_collection = [self.generated_layout, self.select_element, self.input_name, self.pref_subfix] 
            
            cmds.button(label='Rename', 
                        command= functools.partial(self.rename_component, ui_collection, element, self.type_dic.get(type_element)), 
                        bgc = self.background_color, w=175, h=20)
            cmds.rowLayout(parent = self.modular_layout, w= 700, h=50)
            wasafdsa_reew = cmds.text(label = '{}   /   The full name is {}'.format(sentence, element))
    
    def modular_interface(self):      
    
        self.scrollLayout = cmds.scrollLayout('main_scroll_layout')  
       
        self.master_layout = cmds.rowColumnLayout('master_layout', numberOfColumns=1)
        
        cmds.rowColumnLayout(numberOfColumns=6, columnOffset=[(1, 'right', 3), (2, 'right', 3), (3, 'right', 3), (4, 'right', 3), (5, 'right', 3), (6, 'right', 3)], parent = self.master_layout)
        cmds.button(label='List Skin Clusters', command= functools.partial(self.layout_creator, 'skinCluster'))
        cmds.button(label='List Parent Constraints', command= functools.partial(self.layout_creator, 'parentConstraint'))
        cmds.button(label='List Point Constraints', command= functools.partial(self.layout_creator, 'pointConstraint'))
        cmds.button(label='List Orient Constraints', command= functools.partial(self.layout_creator, 'orientConstraint'))
        cmds.button(label='List Aim Constraints', command= functools.partial(self.layout_creator, 'aimConstraint'))
        cmds.button(label='List BlendShapes', command= functools.partial(self.layout_creator, 'blendShape'))
        
        self.lord_layout = cmds.rowLayout('modular_layout', nch=1, parent = self.master_layout)
        self.created_layout = cmds.rowColumnLayout(numberOfColumns=1, columnOffset=[(1, 'right', 3) ], parent = self.lord_layout)
                
        cmds.showWindow()
        
        
test = window_ui()  

test.modular_interface()