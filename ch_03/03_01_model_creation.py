# 03_01_model_creation.py
# GOAL: Create a grid of buttons that will create the different available models in Mobu.
from PySide2.QtWidgets import QApplication, QDialog, QPushButton, QLabel, QGridLayout, QVBoxLayout
from PySide2.QtCore import Qt, Slot
from pyfbsdk import (FBSystem, FBApplication, FBModelCube, FBModelMarker, FBModelNull, FBModelPath3D,
                    FBModelPlane, FBActor, FBActorFace, FBModelOptical, FBCharacter, FBCharacterFace,
                    FBCamera, FBLight, FBNote, FBModelSkeleton, FBModelRoot, FBVector4d, FBColor, FBVector3d)

lsystem = FBSystem()
lscene = lsystem.Scene
lapp = FBApplication()

class ModelCreator(QDialog):
    main_window = QApplication.activeWindow()
    def __init__(self, parent=main_window):
        super(ModelCreator, self).__init__(parent)
        self.setWindowTitle('Model Creator')
        self.setWindowFlags(self.windowFlags() ^ Qt.WindowContextHelpButtonHint)

        self.buttons = []
        title_label = QLabel('Create a new model:', self)

        self.initialize_ui()
        
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(3)
        main_layout.setMargin(3)
        main_layout.addWidget(title_label)
        main_layout.addLayout(self.initialize_layout())


        self.show()

    def initialize_ui(self):
        buttons_text = ["3d Curve", "Camera", "Cube", "Handle", "Light", "Marker", "Note", "Null", "Optical", "Plane", "Skeleton", 
        "Root", "Actor Face", "Actor", "Ch. Extension", "Ch. Face", "Character", "CLEAR"]
        self.buttons = [QPushButton(text, self) for text in buttons_text]

        for i,button in enumerate(self.buttons):
            button.setObjectName(buttons_text[i])
            button.pressed.connect(lambda n=button.objectName(): self.create_fb_model(n))

    def initialize_layout(self):
        layout = QGridLayout(self)
         
        i=0
        for row in range(6):
            for col in range(3):
                button = self.buttons[i]
                if button.objectName() == 'CLEAR':
                    layout.addWidget(button,6,0,1,3)
                else:
                    layout.addWidget(button, row, col)
                i+=1

        return layout

    @Slot()
    def create_fb_model(self, object_name):
        print(f'Creating model... {object_name}')
        if object_name == "3d Curve":
            path = FBModelPath3D("test")
            # After creation, a path always contains 2 default keys
            # At this point, path.PathKeyGetCount() will be 2
            path.Show = True
            # Reposition the 2 default keys
            path.PathKeySet(0, FBVector4d(0, 0, 50, 0))
            path.PathKeySet(1, FBVector4d(50, 0, 0, 0))
            # Add 2 new keys at start and end of the path
            path.PathKeyStartAdd(FBVector4d(0, 0, 100, 0))
            path.PathKeyEndAdd(FBVector4d(100, 0, 0, 0))
            # Insert keys inbetween existing keys
            path.PathKeyInsertAfter(1, FBVector4d(0, 25, 50, 0))
            path.PathKeyInsertAfter(2, FBVector4d(50, 25, 0, 0))
            
        elif object_name == "Camera":
            camera = FBCamera("NewCam")
            camera.Visibility = True
            camera.Show = True
            
            null = FBModelNull("aInterest")
            camera.Interest = null
            
            camera.Translation = FBVector3d(50, 50, 0)

        elif object_name == "Cube":
            cube = FBModelCube("MyCube")
            cube.Show = True
            cube.Scaling = FBVector3d(10, 20, 10)
            cube.Translation = FBVector3d(0, 0, 55)
            print(f'{object_name} created.')

        elif object_name == "Handle":
            pass
        elif object_name == "Light":
            light = FBLight("TheSun")
            light.Show = True
            
            light.Translation = FBVector3d( 120, 100, 70)
        elif object_name == "Marker":
            marker = FBModelMarker("marked")
            marker.Color = FBColor(0.55, 0.8, 0.12)
            marker.Show = True
        elif object_name == "Note":
            cube = FBModelCube("aNotedCube")
            cube.Show = True
            note = FBNote("MyGreetingNote")
            note.Visibility = True
            note.Show = True
            note.StaticComment = "Borja! You are progressing a lot in Mobu Python Scripting."
            note.Color = FBColor(0.65, 0.65, 0)
            note.Attach(cube)
            
        elif object_name == "Null":
            another_null = FBModelNull("anotherNull")
            another_null.Translation = FBVector3d(50, 50, 50)
            
            another_null.Show = True
            
        elif object_name == "Optical":
            optical = FBModelOptical("Optics")
            optical.Show = True
        elif object_name == "Plane":
            plane = FBModelPlane("Planed")
            plane.Show = True
            plane.Scaling = FBVector3d( 5, 1, 5)
            
        elif object_name == "Skeleton":
            skeleton = FBModelSkeleton("DeadBody")
            skeleton.Show = True
            skeleton.Translation = FBVector3d(0, 10, 7)

        elif object_name == "Root":
            root = FBModelRoot("Start Here")
            root.Show = True
        elif object_name == "Actor Face":
            pass
        elif object_name == "Actor":
            pass
        elif object_name == "Ch. Extension":
            pass
        elif object_name == "Ch. Face":
            pass
        elif object_name == "Character":
            pass
        elif object_name == "CLEAR":
            lapp.FileNew()



models = ModelCreator()
