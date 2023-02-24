from pyrosim.commonFunctions import Save_Whitespace

class MATERIAL: 

    def __init__(self, sensor_boolean):

        self.depth  = 3

        # self.string1 = '<material name="Cyan">'

        # self.string2 = '    <color rgba="0 1.0 1.0 1.0"/>'

        # self.string3 = '</material>'

        if sensor_boolean == True:
            color_name = "Green"
            color_rgba = ["0.25", "0.76", "0.50"]
        elif sensor_boolean == False:
            color_name = "Blue"
            color_rgba = ["0.01", "0.54", "1.0"]
        else: # pink color for debugging :)
            color_name = "Pink"
            color_rgba = ["0.75", "0.34", "0.51"] #(190, 86, 131);, 1

        self.string1 = '<material name="' + str(color_name) + '">'
        self.string2 = '    <color rgba="' + color_rgba[0] + ' ' + color_rgba[1] + ' ' + color_rgba[2] + ' 1.0"/>'
        self.string3 = '</material>'


    def Save(self,f):

        Save_Whitespace(self.depth,f)

        f.write( self.string1 + '\n' )

        Save_Whitespace(self.depth,f)

        f.write( self.string2 + '\n' )

        Save_Whitespace(self.depth,f)

        f.write( self.string3 + '\n' )
