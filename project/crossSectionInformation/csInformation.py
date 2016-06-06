'''
Created on 10.03.2016

@author: mkennert
'''
from materialEditor.creater import MaterialCreater
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.slider import Slider
from designClass.design import Design
from materialEditor.iobserver import IObserver
from crossSectionEditor.shapeSelection import ShapeSelection
from crossSectionEditor.doubleTInformation import DoubleTInformation
from crossSectionEditor.rectangleInformation import RectangleInformation

'''
the class CrossSectionInformation was developed to show 
the information of the cs_view
'''
class CrossSectionInformation(GridLayout, IObserver):
    
    #Constructor
    def __init__(self, **kwargs):
        super(CrossSectionInformation, self).__init__(**kwargs)
        self.cols=1
        self.shape=None
        self.firstTimeDoubleT=True
        self.btnSize=Design.btnSize
    
    ########################################################################################################
    # The following part of code create only the graphical user interface                                  #
    ########################################################################################################
    
    '''
    create the gui of the information
    '''
    def createGui(self):
        self.createPopUpShape()
        self.createSelectionMenu()
        self.add_widget(self.rectangleInformation)
        self.createCrossSectionArea()
        self.createAddDeleteArea()
        self.createMaterialInformation()
        self.createAddLayerInformationArea()
        self.createConfirmCancelArea()
    
    '''
    create the layout where you can select the cross-section-shape
    '''
    def createSelectionMenu(self):
        selectionContent=GridLayout(cols=1,spacing=10, 
                                    size_hint_y=None,row_force_default=True, 
                                    row_default_height=self.btnSize)
        self.btnSelection=Button(text='rectangle',size_hint_y=None, height=self.btnSize,
                                  size_hint_x=None, width=200)
        self.btnSelection.bind(on_press=self.showShapeSelection)
        selectionContent.add_widget(self.btnSelection)
        self.add_widget(selectionContent)
    
    '''
    create popup where you can select the shape of the cross section
    '''
    def createPopUpShape(self):
        shapeContent=ShapeSelection()
        shapeContent.setInformation(self)
        self.shapeSelection=Popup(title='shape',content=shapeContent)        
        
    '''
    the method createAddDeleteArea create the area where you can 
    add new materials and delete materials from the cs_view
    '''
    def createAddDeleteArea(self):
        self.btnArea=BoxLayout(orientation='horizontal')
        addBtn=Button(text='add layer',size_hint_y=None, height=self.btnSize)
        addBtn.bind(on_press=self.showAddLayerArea)
        deleteBtn=Button(text='delete layer',size_hint_y=None, height=self.btnSize)
        deleteBtn.bind(on_press=self.deleteLayer)
        self.btnArea.add_widget(addBtn)
        self.btnArea.add_widget(deleteBtn)
        self.add_widget(self.btnArea)
    
    '''
    the method createMaterialInformation create the area where you can 
    see the information about the selected materials
    '''

    def createMaterialInformation(self):
        self.materialArea = GridLayout(cols=1)
        self.materialName = Label(text='-')
        self.materialPrice = Label(text='-')
        self.materialDensity = Label(text='-')
        self.materialStiffness = Label(text='-')
        self.materialStrength = Label(text='-')
        self.materialPercent = Label(text='10 %')
        labelLayout = GridLayout(cols=4)
        labelLayout.add_widget(Label(text='name:'))
        labelLayout.add_widget(self.materialName)
        labelLayout.add_widget(Label(text='price:'))
        labelLayout.add_widget(self.materialPrice)
        labelLayout.add_widget(Label(text='density:'))
        labelLayout.add_widget(self.materialDensity)
        labelLayout.add_widget(Label(text='stiffness:'))
        labelLayout.add_widget(self.materialStiffness)
        labelLayout.add_widget(Label(text='tensile strength:'))
        labelLayout.add_widget(self.materialStrength)
        labelLayout.add_widget(Label(text='percent:'))
        labelLayout.add_widget(self.materialPercent)
        self.percentValue = Slider(min=0.05, max=0.2, value=0.1)
        self.percentValue.bind(value=self.setPercent)
        self.materialArea.add_widget(labelLayout)
        self.materialArea.add_widget(self.percentValue)
        self.add_widget(self.materialArea)
    
    '''
    the method createCrossSectionArea create the area where you can 
    see the information of the cs_view
    '''
    def createCrossSectionArea(self):
        self.crossSectionPrice=Label(text='-')
        self.crossSectionWeight=Label(text='-')
        self.crossSectionStrength=Label(text='-')
        self.crossSectionArea=GridLayout(cols=2)
        self.crossSectionArea.add_widget(Label(text='price [Euro/m]:'))
        self.crossSectionArea.add_widget(self.crossSectionPrice)
        self.crossSectionArea.add_widget(Label(text='weight [kg]:'))
        self.crossSectionArea.add_widget(self.crossSectionWeight)
        self.crossSectionArea.add_widget(Label(text='tensile strength [MPa]:'))
        self.crossSectionArea.add_widget(self.crossSectionStrength)
        self.add_widget(self.crossSectionArea)
    
    '''
    the method createAddLayerInformationArea create the area where you can 
    add new materials
    '''
    def createAddLayerInformationArea(self):
        self.createMaterialOptions()
        self.addingMaterialArea=GridLayout(cols=2)
        self.addingMaterialArea.add_widget(Label(text='Material:'))
        self.materialOption=Button(text='steel',size_hint_y=None, height=self.btnSize)
        self.materialOption.bind(on_release=self.popup.open)
        self.addingMaterialArea.add_widget(self.materialOption)
        self.materialPercentWhileCreating=Label(text='percent: 10%')
        self.addingMaterialArea.add_widget(self.materialPercentWhileCreating)
        self.sliderLayerPercent=Slider(min=0.05,max=0.2,value=0.1)
        self.sliderLayerPercent.bind(value=self.setPercenetWhileCreating)
        self.addingMaterialArea.add_widget(self.sliderLayerPercent)
    
    '''
    the method createMaterialOptions create the popup where you can 
    select the materials for the new layer
    '''
    def createMaterialOptions(self):
        self.layoutMaterials=GridLayout(cols=3)
        self.materialEditor=MaterialCreater()
        self.materialEditor.signInParent(self)
        self.popupMaterialEditor=Popup(title='editor',content=self.materialEditor)
        for i in range(0,self.allMaterials.getLength()):
            btnMaterialA=Button(text=self.allMaterials.allMaterials[i].name)
            btnMaterialA.bind(on_press=self.selectMaterial)
            self.layoutMaterials.add_widget(btnMaterialA)
        self.btnMaterialEditor=Button(text='create material')
        self.btnMaterialEditor.bind(on_press=self.popupMaterialEditor.open)
        self.layoutMaterials.add_widget(self.btnMaterialEditor)
        self.popup=Popup(title='materials',content=self.layoutMaterials)
    
    '''
    the method createConfirmCancelArea create the area where you can 
    confirm your creation of the new materials or cancel the creation
    '''
    def createConfirmCancelArea(self):
        self.confirmCancelArea=BoxLayout()
        confirmBtn=Button(text='confirm',size_hint_y=None, height=self.btnSize)
        confirmBtn.bind(on_press=self.addLayer)
        cancelBtn=Button(text='cancel',size_hint_y=None, height=self.btnSize)
        cancelBtn.bind(on_press=self.cancelAdding)
        self.confirmCancelArea.add_widget(confirmBtn)
        self.confirmCancelArea.add_widget(cancelBtn)
    
    ########################################################################################################
    ########################################################################################################
    
    '''
    the method showAddLayerArea was developed to show the 
    the addingMaterialArea and hide the material_information
    '''
    def showAddLayerArea(self, button):
        self.remove_widget(self.materialArea)
        self.remove_widget(self.btnArea)
        self.sliderLayerPercent.value=0.1
        self.add_widget(self.addingMaterialArea,0)
        self.add_widget(self.confirmCancelArea, 1)
    
    '''
    the method finishedAdding was developed to hide the 
    the addingMaterialArea and show the materialArea
    '''
    def finishedAdding(self):
        self.remove_widget(self.addingMaterialArea)
        self.remove_widget(self.confirmCancelArea)
        self.add_widget(self.materialArea,0)
        self.add_widget(self.btnArea,1)
    
    '''
    the method addLayer add a new layer at the cross section
    it use the choosen percent value
    '''
    def addLayer(self,button):
        self.finishedAdding()
        for i in range(0,self.allMaterials.getLength()):
            if self.allMaterials.allMaterials[i].name==self.materialOption.text:
                self.cs.addLayer(self.sliderLayerPercent.value,self.allMaterials.allMaterials[i])
                return
    '''
    the method cancelAdding would be must call when the user wouldn't 
    add a new materials
    '''
    def cancelAdding(self,button):
        self.finishedAdding()
    
    '''
    the method deleteLayer was developed to delete a existing
    materials
    '''
    def deleteLayer(self, button):
        self.cs.deleteLayer()
    
    '''
    the method updateLayerInformation was developed to update
    the information, when the user selected a other rectangle in the view
    '''
    def updateLayerInformation(self,name,price,density,stiffness,strength,percent):
        self.materialName.text=str(name)
        self.materialPrice.text=str(price)
        self.materialDensity.text=str(density)
        self.materialStiffness.text=str(stiffness)
        self.materialStrength.text=str(strength)
        self.percentValue.value=percent
    
    '''
    the method updateCrossSectionInformation update the cross section information.
    '''
    def updateCrossSectionInformation(self,price, weight,strength):
        self.crossSectionPrice.text=str(price)
        self.crossSectionWeight.text=str(weight)
        self.crossSectionStrength.text=str(strength)
    
    '''
    the method cancelEditMaterial cancel the editing of the material
    and reset the values of the materialEditor
    '''
    def cancelEditMaterial(self):
        self.popupMaterialEditor.dismiss()
        self.materialEditor.resetEditor()
        
    '''
    the method update_materials update the view of the materials. 
    its make sure that the create material button is the last component 
    of the gridlayout
    '''
    def update(self):
        self.layoutMaterials.remove_widget(self.btnMaterialEditor)
        btnMaterialA=Button(text=self.allMaterials.allMaterials[-1].name)
        btnMaterialA.bind(on_press=self.selectMaterial)
        self.layoutMaterials.add_widget(btnMaterialA)
        self.layoutMaterials.add_widget(self.btnMaterialEditor)
        
    '''
    look which shape the user has selected
    '''
    def finishedShapeSelection(self,btn):
        if btn.text=='circle':
            #not finished yet
            pass
        elif btn.text=='rectangle':
            self.setRectangle(btn)
        elif btn.text=='doubleT':
            self.setDoubleT(btn)
    
    '''
    open the popup where the user can select the shape
    ''' 
    def showShapeSelection(self,btn):
        self.shapeSelection.open()
    
    #################################################################################################
    #                                Setter && Getter                                               #
    #################################################################################################
    
    '''
    the method will be called when the user selected a material
    the popup will be closed and the button text change to the material
    name
    '''
    def selectMaterial(self, Button):
        self.popup.dismiss()
        self.materialOption.text=Button.text
    
    '''
    the method setPercent change the percentage share 
    of the materials. 
    Attention: this method must be call when the materials already exist
    '''
    def setPercent(self, instance, value):
        self.cs.setPercent(value)
        self.materialPercent.text=str(int(value*100))+' %'
    
    '''
    the method setPercenetWhileCreating change the percentage share 
    of the materials. Attention: this method must be call 
    when the materials isn't exist
    '''
    def setPercenetWhileCreating(self,instance,value):
        self.materialPercentWhileCreating.text='percent: '+str(int(value*100))+' %'
    
    '''
    the method setCrossSection was developed to say the view, 
    which cross section should it use
    '''
    def setCrossSection(self,allCrossSections):
        self.allCrossSections=allCrossSections
        #default cross section rectangle
        self.cs=allCrossSections.getCSRectangle()
        self.rectangleInformation=RectangleInformation()
        self.shape=self.rectangleInformation
        self.rectangleInformation.setCrossSection(self.cs)
        self.allMaterials=self.allCrossSections.allMaterials
        self.allMaterials.addListener(self)
        self.createGui()
    
    '''
    change the current cross section
    '''
    def changeCrossSection(self,cross_section):
        self.cs=cross_section
        
    '''
    show the rectangle shape
    '''
    def setRectangle(self, btn):
        self.btnSelection.text=btn.text
        self.cs=self.allCrossSections.getCSRectangle()
        self.remove_widget(self.shape)
        self.shape=self.rectangleInformation
        self.add_widget(self.rectangleInformation,3)
        self.allCrossSections.setRectangleView()
        self.shapeSelection.dismiss()
    
    '''
    show the doubleT shape
    '''
    def setDoubleT(self,btn):
        self.btnSelection.text=btn.text
        self.cs=self.allCrossSections.getCSDoubleT()
        if self.firstTimeDoubleT:
            self.doubleTInformation=DoubleTInformation()
            self.doubleTInformation.setCrossSection(self.cs)
            self.firstTimeDoubleT=False
        self.remove_widget(self.shape)
        self.shape=self.doubleTInformation
        self.add_widget(self.doubleTInformation,3)
        self.allCrossSections.setDoubleTView()
        self.shapeSelection.dismiss()
    
    '''
    show the circle shape
    '''
    #not finished yet
    def setCircle(self,btn):
        self.btnSelection.text=btn.text
        #not finished yet
        #self.cs=self.allCrossSections.getCSCircle()
        self.shapeSelection.dismiss()
    
