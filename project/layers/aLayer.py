'''
Created on 09.05.2016

@author: mkennert
'''
class ALayer:
    '''
    check if the mouse is in the rectangle
    return true, if the mouse is within, otherwise return false
    '''
    def mouseWithin(self, x, y):
        raise NotImplemented('not implemented')
    
    '''
    check if the mouse is in the rectangle
    return true, if the mouse is within, otherwise return false
    Attention: it checks only the x_coordinate. this method
    was developed to make the the movement of the layer faster
    '''
    def mouseWithinX(self, x):
        raise NotImplemented('not implemented')
    
    '''
    the method setYCoordinate change the y of the small_keyboard-rectangle
    '''
    def setYCoordinate(self, value):
        self.y = value

    '''
    the method setMaterial was developed to set the small_keyboard the materials
    '''
    def setMaterial(self, material):
        self.material = material

    '''
    return the materials information
    '''
    def getMaterialInformations(self):
        return [self.material.name, self.material.price, self.material.density, self.material.stiffness, self.material.strength]

    '''
    must return the weight of the layer
    '''
    def getWeight(self):
        raise NotImplemented('not implemented')

    '''
    return the strain of the layer
    '''
    def getStrain(self):
        return self.material.strength / self.material.stiffness
    
    '''
    the method to change the percent
    '''
    def setPercentage(self, value):
        self.percent = value