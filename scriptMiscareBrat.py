import bpy
import serial
import threading
import time

# Definim Portul Serial 
port = 'COM4'
baud_rate = 9600

# Deschidem conectiunea serial
ser = serial.Serial(port, baud_rate)

# Oferim putin timp pentru ca conectiunea sa fie stabilita
time.sleep(2)

# Definim oasele 
bone_name = "hand.R"
bone_name2 = "lowerarm.R"
bone_name3 = "upperarm.R"

# cream un obiect din armatura modelului 3D
armature = bpy.data.objects['Armature']  

# Creez o functie pentru a mapa valorile din Arduino la cele din Blender
def map_value(value, from_min, from_max, to_min, to_max):
    return (value - from_min) * (to_max - to_min) / (from_max - from_min) + to_min

# Functia care citeste valorile potentiometrelor pe portul serial
# Si care apoi modifica pozitiile oaselor respective
def update_bone_rotation():
    # Citirea valorilor de pe portul serial
    try:
        line = ser.readline().decode('utf-8').strip()
        
        # Punerea valoriilor intr-un Array
        pot_values = line.split()
        
        # Extragem valorile potentiometrelor A0 , A3 si A4
        a4_value = int(pot_values[4])
        a3_value = int(pot_values[3])
        a0_value = int(pot_values[0])
        
        
        # Mapam valorile potentiometrelor intr-o arie suportata de Blender
        # Mapam 0 - 180 la -1.57 - 1.57 radiani (-90 , 90 de grade aproximativ)
        mapped_value1 = map_value(a4_value, 0, 180, -1.57, 1.57)
        mapped_value2 = map_value(a3_value, 0, 180, 0, 1.57)
        mapped_value3 = map_value(a0_value, 0, 180, -1.57, 1.57)
        
        # Setam roatie oaselor
        bpy.context.view_layer.objects.active = armature
        
        # Accesam direct datele oaselor fara a mai schimba modul din Blender
        bone1 = armature.pose.bones[bone_name]
        bone1.rotation_mode = 'XYZ'
        bone1.rotation_euler[0] = mapped_value1  
        
        bone2 = armature.pose.bones[bone_name2]
        bone2.rotation_mode = 'XYZ'
        bone2.rotation_euler[0] = mapped_value2  
        
        bone3 = armature.pose.bones[bone_name3]
        bone3.rotation_mode = 'XYZ'
        bone3.rotation_euler[0] = mapped_value3 
        
        # Updatam Blender cu modificarile
        bpy.context.view_layer.update()
    
    except Exception as e:
        print(f"Error reading from serial or updating bone: {e}")

# Functie care improspateaza constant pozitiile oaselor
def update_callback():
    
    update_bone_rotation()
    # Functia va rula din nou dupa 0.1 secunde
    return 0.1

# Incepem procesul de improspatare
bpy.app.timers.register(update_callback)

# Oprim timer-ul si oprim scriptul cand Blender este oprit
def cleanup():
    ser.close()
    bpy.app.timers.unregister(update_callback)




