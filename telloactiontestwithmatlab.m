drone = ryze();
disp(drone.BatteryLevel);

cameraObj = camera(drone);
preview(cameraObj)

takeoff(drone);
move(drone,[0.2 0.3 0.5],'Speed',0.5);    %units:Meter Meter/Second
turn(drone,deg2rad(90));            %turn 90 degrees clockwise
land(drone);