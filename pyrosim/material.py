from pyrosim.commonFunctions import Save_Whitespace

class MATERIAL: 

    def __init__(self, sensor_boolean):

        self.depth  = 3

        # self.string1 = '<material name="Cyan">'

        # self.string2 = '    <color rgba="0 1.0 1.0 1.0"/>'

        # self.string3 = '</material>'

        if sensor_boolean:
            color_name = "Green"
            color_rgba = ["0.0", "1.0", "0.0"]
        else:
            color_name = "Blue"
            color_rgba = ["0.0", "0.0", "1.0"]

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
