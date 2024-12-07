from hardware.PCA9685Actuator      import PCA9685Actuator
from hardware.ServoActuator        import ServoActuator
from controllers.config_controller import ConfigController

class ServoRegistry:
    _instance = None

    def __init__(self):
        if not ServoRegistry._instance:
            self.config_controller  = ConfigController.get_instance()
            self.config             = self.config_controller.get_config()
            self.pwm                = PCA9685Actuator(0x40, debug=False)
            self.pwm.setPWMFreq(50)
            self.servos             = self._create_servos()
            ServoRegistry._instance = self
        else:
            raise Exception("You cannot create another ServoRegistry class")

    def _create_servos(self):
        servos = {
        'front_right_pitch':    ServoActuator(id=int(self.config['front_right_pitch_id']),    name='Front_Right_Pitch_Servo',    min_angle=-30, max_angle=90, offset=int(self.config['front_right_pitch_offset']),    neutral_angle=0, is_reversed=bool(self.config['front_right_pitch_rev']),   pwm=self.pwm),
        'front_right_shoulder': ServoActuator(id=int(self.config['front_right_shoulder_id']), name='Front_Right_Shoulder_Servo', min_angle=-45, max_angle=45, offset=int(self.config['front_right_shoulder_offset']), neutral_angle=0, is_reversed=bool(self.config['front_right_shoulder_rev']),pwm=self.pwm),
        'front_right_knee':     ServoActuator(id=int(self.config['front_right_knee_id']),     name='Front_Right_Knee_Servo',     min_angle=-90, max_angle=75, offset=int(self.config['front_right_knee_offset']),     neutral_angle=0, is_reversed=bool(self.config['front_right_knee_rev']),    pwm=self.pwm),

        'front_left_pitch':     ServoActuator(id=int(self.config['front_left_pitch_id']),     name='Front_Left_Pitch_Servo',     min_angle=-30, max_angle=90, offset=int(self.config['front_left_pitch_offset']),     neutral_angle=0, is_reversed=bool(self.config['front_left_pitch_rev']),    pwm=self.pwm),
        'front_left_shoulder':  ServoActuator(id=int(self.config['front_left_shoulder_id']),  name='Front_Left_Shoulder_Servo',  min_angle=-45, max_angle=45, offset=int(self.config['front_left_shoulder_offset']),  neutral_angle=0, is_reversed=bool(self.config['front_left_shoulder_rev']), pwm=self.pwm),
        'front_left_knee':      ServoActuator(id=int(self.config['front_left_knee_id']),      name='Front_Left_Knee_Servo',      min_angle=-90, max_angle=75, offset=int(self.config['front_left_knee_offset']),      neutral_angle=0, is_reversed=bool(self.config['front_left_knee_rev']),     pwm=self.pwm),

        'back_right_pitch':     ServoActuator(id=int(self.config['back_right_pitch_id']),     name='Back_Right_Pitch_Servo',     min_angle=-30, max_angle=90, offset=int(self.config['back_right_pitch_offset']),     neutral_angle=0, is_reversed=bool(self.config['back_right_pitch_rev']),    pwm=self.pwm),
        'back_right_shoulder':  ServoActuator(id=int(self.config['back_right_shoulder_id']),  name='Back_Right_Shoulder_Servo',  min_angle=-75, max_angle=45, offset=int(self.config['back_right_shoulder_offset']),  neutral_angle=0, is_reversed=bool(self.config['back_right_shoulder_rev']), pwm=self.pwm),
        'back_right_knee':      ServoActuator(id=int(self.config['back_right_knee_id']),      name='Back_Right_Knee_Servo',      min_angle=-90, max_angle=75, offset=int(self.config['back_right_knee_offset']),      neutral_angle=0, is_reversed=bool(self.config['back_right_knee_rev']),     pwm=self.pwm),

        'back_left_pitch':      ServoActuator(id=int(self.config['back_left_pitch_id']),      name='Back_Left_Pitch_Servo',      min_angle=-30, max_angle=90, offset=int(self.config['back_left_pitch_offset']),      neutral_angle=0, is_reversed=bool(self.config['back_left_pitch_rev']),     pwm=self.pwm),
        'back_left_shoulder':   ServoActuator(id=int(self.config['back_left_shoulder_id']),   name='Back_Left_Shoulder_Servo',   min_angle=-75, max_angle=45, offset=int(self.config['back_left_shoulder_offset']),   neutral_angle=0, is_reversed=bool(self.config['back_left_shoulder_rev']),  pwm=self.pwm),
        'back_left_knee':       ServoActuator(id=int(self.config['back_left_knee_id']),       name='Back_Left_Knee_Servo',       min_angle=-90, max_angle=75, offset=int(self.config['back_left_knee_offset']),       neutral_angle=0, is_reversed=bool(self.config['back_left_knee_rev']),      pwm=self.pwm)
        }
        
        return servos

    def get_servos(self):
        """Return the existing servo instances."""
        return self.servos

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = ServoRegistry()
        return cls._instance

    def get_servo_names(self):
        """Return a list of the names of all servos in the registry."""
        return list(self.get_servos().keys())

    def refresh_servos(self):
        """Destroy existing servo objects, reload config, and recreate servos."""
        # 1) Destroy any objects in `self.servos`
        self.servos.clear()
        # 2) Reload the config data
        self.config = self.config_controller.get_config()
        # 3) Recreate the list of servos
        self.servos = self._create_servos()
         
