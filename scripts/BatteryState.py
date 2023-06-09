#!/usr/bin/env python
# license removed for brevity
import rospy
import random
from std_msgs.msg import Bool
import roslaunch 
#from assignment1 import Empty
from std_srvs.srv import Empty
from assignment1.msg import PlanningAction,PlanningResult,PlanningGoal
from assignment2.srv import PlanningSrv, PlanningSrvResponse
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal, MoveBaseFeedback, MoveBaseResult
import actionlib
batteryduration=720

def BatteryState():
    client = actionlib.SimpleActionClient('/move_base', MoveBaseAction)
    pub = rospy.Publisher('BatteryState', Bool, queue_size=10)
    """client = actionlib.SimpleActionClient("move_to_position", PlanningAction)
    client.wait_for_server()"""
    rate = rospy.Rate(1) # 1 hz
    batterylevel = batteryduration
    batteryBool = True
    CanCancelFlag = True ## when the battery is empty, the robot can cancel the current goal but not the next one (going to the charging station)
    while not rospy.is_shutdown():
        ImCharging = rospy.get_param('IsChargingParam')
        #ImCharging = True
        if (not ImCharging) and (batterylevel > 0): #discharging 
            batterylevel = batterylevel - 1
            if batterylevel < 7:
                rospy.loginfo("Battery is going too low")
            #batteryBool = True
            
        elif (not ImCharging) and (batterylevel == 0): #Battery is empty
            batteryBool = False
            #client.cancel_all_goals()
            if CanCancelFlag: 
                client.cancel_all_goals()
                CanCancelFlag = False
                rospy.loginfo("Battery is empty, preempting current goal, going to charge station")
            rospy.loginfo("WARNING: Battery is empty")
        
        elif ImCharging and (batterylevel <= batteryduration): #charging 
            if batterylevel == batteryduration:
                rospy.loginfo("Battery is full")
                CanCancelFlag = True
                batteryBool = True
            else:
                batterylevel = batterylevel + 10 ## irrealistic but useful for do not wait too much in the simulation
                rospy.loginfo("Charging")
	
        rospy.loginfo("Battery level:" + str(batterylevel)) #batteryBool
        pub.publish(batteryBool)
        rate.sleep()

if __name__ == '__main__':
    
    try:
        rospy.init_node('batterystatus', anonymous=True)#, anonymous=True
        BatteryState()
    except rospy.ROSInterruptException:
        pass
