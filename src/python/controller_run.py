# import multiprocessing as mp
from lib.cartpolecontroller import CartPoleController
from lib.cartpolesimulator import CartPoleEnvSimulator, CartPoleSerialSimulator
from lib.cartpolesystem import CartPoleStepperMotorSystem, Pole, Cart
from lib.motors import StepperMotor
from serial.tools.list_ports import comports

def main():
    # mp.set_start_method('spawn')
    
    dt = 0.01
    g = 9.81
    r = 0.04456
    x_max = 1.15/2
    l1 = 0.225
    m1 = 0.0446
    m = 0.2167
    
    cart = Cart(m, 0.01, (-x_max, x_max), 0.1)
    motor = StepperMotor(r, (-2.5, 2.5), 0.2, (-2.5, 2.5), 0.1)
    poles = [Pole(m1, l1, 0.001)]
    system = CartPoleStepperMotorSystem(cart, motor, poles, g)

    if (input("Simulate (y/n)?") == "y"):
        sim = CartPoleEnvSimulator(dt, system)
        controller = CartPoleController(sim, dt)
        sim.run()
        controller.run()
    else:
        sim = CartPoleSerialSimulator(dt, system)
        controller = CartPoleController(sim, dt)
        # open ports
        print("Available ports: ")
        ports = [port.name for port in comports()]
        if len(ports) == 0:
            raise ValueError("No ports available")

        for port in ports:
            print(port)

        port = input(f"Port ({ports[0]}): ")
        if port == "":
            port = ports[0]
        sim.run(port, 500000)
        controller.run()

if __name__ == '__main__':
    main()