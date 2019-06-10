import pygame
import cv2
from controle_drone import controleDrone
from djitellopy import Tello

controle = controleDrone()
tello = Tello()
activateCamera = True

if activateCamera:
    tello.streamon()
    cap = cv2.VideoCapture(tello.get_udp_video_address())

def get_joystick_axes():
    joystick_count = pygame.joystick.get_count()
    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()
        numButton = get_joystick_button(joystick=joystick)
        buttonControll(numButton)
        axes = []
        for i in range(0,4):
            axes.append(round(pygame.joystick.Joystick(0).get_axis(i), 2))
    return axes

def get_joystick_button(joystick):
    buttons = joystick.get_numbuttons()
    for i in range(buttons):
        button = joystick.get_button(i)
        if button != 0:
            return i

def buttonControll(numButton):
    if numButton == 0:
        tello.takeoff()
    elif numButton == 2:
        tello.land()

def axesStop(axe_number):
    speed = 100
    if axe_number == -0.0:
        return 0

    elif axe_number < 0.0:
        return int((axe_number * speed) * -1)

    else:
        return int((axe_number * speed) * -1)

def destroyCamera():
    if activateCamera:
        cap.release()
        cv2.destroyAllWindows()

def main():
    #screen = pygame.display.set_mode((500, 500))
    pygame.joystick.init()
    endGame = False
    connect = tello.connect()
    print('Entrei aqui')
    #frame_read = tello.get_frame_read()

    while not(endGame):

        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.K_q:
                endGame = True
                destroyCamera()


        key_pressed = pygame.key.get_pressed()

        if key_pressed[pygame.K_q]:
            endGame = True
            destroyCamera()

        if pygame.joystick.get_count():
            axes = {
                'y': axesStop(get_joystick_axes()[1]),
                'x': axesStop(get_joystick_axes()[0] * -1),
                'a': axesStop(get_joystick_axes()[3]),
                'b': axesStop(get_joystick_axes()[2])
            }
            if connect:
                tello.send_rc_control(axes['b'], axes['a'], axes['y'], axes['x'])
            print(axes)
        else:
            print('Controle off')

        if activateCamera:
            ret, frame = cap.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cv2.imshow('frame', gray)

        #pygame.display.update()


if __name__ == '__main__':
    main();