import sensingsp as ssp
import numpy as np
from mathutils import Vector
# import matplotlib
# matplotlib.use('Qt5Agg')
from matplotlib import pyplot as plt
import cv2
import os
import bpy
def make_simple_scenario():
    predefine_movingcube_6843()
def run_simple_chain():
    processing_1()
def predefine_movingcube_6843(interpolation_type='LINEAR'):
    #     Blender provides several interpolation types, and as of recent versions, there are 6 main interpolation options:

    # CONSTANT ('CONSTANT')
    # The value remains constant between keyframes, resulting in a stepped change at each keyframe.
    # LINEAR ('LINEAR')
    # The value changes linearly between keyframes, resulting in a straight transition between the keyframe points.
    # BEZIER ('BEZIER')
    # The value follows a bezier curve between keyframes, allowing for smooth transitions with adjustable handles for fine control over the curve.
    # SINE ('SINE')
    # The value follows a sine curve between keyframes, creating smooth, wave-like transitions.
    # QUAD ('QUAD')
    # The value follows a quadratic curve, which can create an accelerating or decelerating effect.
    # CUBIC ('CUBIC')
    # The value follows a cubic curve between keyframes, providing a slightly more complex smooth transition than quadratic.
    ssp.utils.delete_all_objects()
    ssp.utils.define_settings()
    cubex = ssp.environment.add_cube(location=Vector((2.7, np.sqrt(3**2-2.7**2), 0)), direction=Vector((1,0, 0)), scale=Vector((.1, .1, .1)), subdivision=0)
    cubex["RCS0"]=1
    cube = ssp.environment.add_cube(location=Vector((0, 0, 0)), direction=Vector((1, 0, 0)), scale=Vector((.1, .1, .1)), subdivision=0)
    cube["RCS0"]=1
    cube.location = (3,0,0)
    cube.keyframe_insert(data_path="location", frame=1)
    cube.location = (3, 3,0)
    cube.keyframe_insert(data_path="location", frame=30)
    cube.location = (3, -3,0)
    cube.keyframe_insert(data_path="location", frame=100)
    for fcurve in cube.animation_data.action.fcurves:
        for keyframe in fcurve.keyframe_points:
            keyframe.interpolation = interpolation_type
    ssp.integratedSensorSuite.define_suite(0, location=Vector((0, 0, 0)), rotation=Vector((0, 0, 0)))
    
    
    radar = ssp.radar.utils.predefined_array_configs_TI_IWR6843(isuite=0, iradar=0, location=Vector((0, 0,0)), rotation=Vector((np.pi/2,0, -np.pi/2)), f0=70e9)
    # radar = ssp.radar.utils.predefined_array_configs_TI_IWR6843_az(isuite=0, iradar=0, location=Vector((0, 0,0)), rotation=Vector((np.pi/2,0, -np.pi/2)), f0=70e9)
    # radar = ssp.radar.utils.predefined_array_configs_LinearArray(isuite=0, iradar=0, location=Vector((0, 0,0)), rotation=Vector((np.pi/2,0, -np.pi/2)), f0=70e9,LinearArray_TXPos=[0],LinearArray_RXPos=[i*3e8/70e9/2 for i in range(30)])
    
    
    
    # radar['RF_AnalogNoiseFilter_Bandwidth_MHz']=0
    
    ssp.utils.set_frame_start_end(start=1,end=2)
    ssp.utils.useCUDA()
    # print(f"rangeResolution maxUnambigiousRange = {ssp.radar.utils.rangeResolution_and_maxUnambigiousRange(radar)}")

def predefine_TruckHuman_SameRG():
    ssp.utils.delete_all_objects()
    if 0:
        ssp.utils.open_Blend(os.path.join(ssp.config.temp_folder, "TruckHuman.blend"))
    # ssp.utils.open_Blend(os.path.join(ssp.config.temp_folder, "SimpleCube_y05.blend"))
    else:
        cube = ssp.environment.add_cube(location=Vector((20, 0, 0)), direction=Vector((1, 0, 0)), scale=Vector((.1, .1, .1)), subdivision=0)
        cube["RCS0"]=1e5
        t=np.deg2rad(2)
        cube = ssp.environment.add_cube(location=Vector((20*np.cos(t), 20*np.sin(t), 0)), direction=Vector((1, 0, 0)), scale=Vector((.1, .1, .1)), subdivision=0)
        cube["RCS0"]=1e5
        # cube.location = (20,0,0)
        # cube.keyframe_insert(data_path="location", frame=1)
        # cube.location = (20, 3,0)
        # cube.keyframe_insert(data_path="location", frame=50)
        # cube.location = (20, 0,0)
        # cube.keyframe_insert(data_path="location", frame=100)
        
    
    ssp.utils.define_settings()
    ssp.integratedSensorSuite.define_suite(0, location=Vector((0, 0, 0)), rotation=Vector((0, 0, 0)))
    radar = ssp.radar.utils.predefined_array_configs_DARWu(isuite=0, iradar=0, location=Vector((0, 0,0)), rotation=Vector((np.pi/2,0, -np.pi/2)), f0=70e9)
    # radar = ssp.radar.utils.predefined_array_configs_TI_IWR6843(isuite=0, iradar=0, location=Vector((0, 0,0)), rotation=Vector((np.pi/2,0, -np.pi/2)), f0=70e9)
    # radar = ssp.radar.utils.predefined_array_configs_LinearArray(isuite=0, iradar=0, location=Vector((0, 0,0)), rotation=Vector((np.pi/2,0, -np.pi/2)), 
    #                                                              f0=70e9
    #                                                              ,LinearArray_TXPos =[(i)*4*3e8/70e9/2 for i in range(1)],
    #                                                             LinearArray_RXPos =[(i+10)*3e8/70e9/2 for i in range(4)])
    # radar = ssp.radar.utils.predefined_array_configs_SISO(isuite=0, iradar=0, location=Vector((0, 0,0)), rotation=Vector((np.pi/2,0, -np.pi/2)), f0=70e9)
    
    Res,MaxR =    ssp.radar.utils.rangeResolution_and_maxUnambigiousRange(radar)
    radar['RF_AnalogNoiseFilter_Bandwidth_MHz']=2
    radar['DopplerProcessingMIMODemod']='Simple'
    radar['ADC_levels']=256*8
    radar['RangeFFT_OverNextP2']=1
    radar['DopplerFFT_OverNextP2']=0
    radar['AzFFT_OverNextP2']=5
    radar['NPulse']=6*64
    
# specifications['RangeFFT_OverNextP2'] = radarobject['GeneralRadarSpec_Object']['RangeFFT_OverNextP2']
# specifications['DopplerFFT_OverNextP2'] = radarobject['GeneralRadarSpec_Object']['']
# specifications['AzFFT_OverNextP2'] = radarobject['GeneralRadarSpec_Object']['AzFFT_OverNextP2']
# specifications['ElFFT_OverNextP2'] = radarobject['GeneralRadarSpec_Object']['ElFFT_OverNextP2']

    ssp.utils.set_frame_start_end(start=1,end=40)
    ssp.utils.useCUDA()
    ssp.utils.trimUserInputs() 
    ssp.config.restart()
    ssp.config.DopplerProcessingMethod_FFT_Winv = (True)

    ssp.config.directReceivefromTX =  False 
    ssp.config.RadarRX_only_fromscatters_itsTX = True
    ssp.config.RadarRX_only_fromitsTX = True
    ssp.config.Radar_TX_RX_isolation = True
    ssp.utils.save_Blender()
def predefine_TruckHuman_DiffRG():
    ssp.utils.delete_all_objects()
    if 1:
        ssp.utils.open_Blend(os.path.join(ssp.config.temp_folder, "TruckHumanModified.blend"))
    # ssp.utils.open_Blend(os.path.join(ssp.config.temp_folder, "SimpleCube_y05.blend"))
    else:
        cube = ssp.environment.add_cube(location=Vector((20, 20, 0)), direction=Vector((1, 0, 0)), scale=Vector((.1, .1, .1)), subdivision=0)
        cube["RCS0"]=1e6
        # cube.location = (20,0,0)
        # cube.keyframe_insert(data_path="location", frame=1)
        # cube.location = (20, 3,0)
        # cube.keyframe_insert(data_path="location", frame=50)
        # cube.location = (20, 0,0)
        # cube.keyframe_insert(data_path="location", frame=100)
        
    
    ssp.utils.define_settings()
    ssp.integratedSensorSuite.define_suite(0, location=Vector((0, 0, 0)), rotation=Vector((0, 0, 0)))
    radar = ssp.radar.utils.predefined_array_configs_DARWu(isuite=0, iradar=0, location=Vector((0, 0,0)), rotation=Vector((np.pi/2,0, -np.pi/2)), f0=70e9)
    # radar = ssp.radar.utils.predefined_array_configs_TI_IWR6843(isuite=0, iradar=0, location=Vector((0, 0,0)), rotation=Vector((np.pi/2,0, -np.pi/2)), f0=70e9)
    # radar = ssp.radar.utils.predefined_array_configs_LinearArray(isuite=0, iradar=0, location=Vector((0, 0,0)), rotation=Vector((np.pi/2,0, -np.pi/2)), 
    #                                                              f0=70e9
    #                                                              ,LinearArray_TXPos =[(i)*4*3e8/70e9/2 for i in range(1)],
    #                                                             LinearArray_RXPos =[(i+10)*3e8/70e9/2 for i in range(4)])
    # radar = ssp.radar.utils.predefined_array_configs_SISO(isuite=0, iradar=0, location=Vector((0, 0,0)), rotation=Vector((np.pi/2,0, -np.pi/2)), f0=70e9)
    
    Res,MaxR =    ssp.radar.utils.rangeResolution_and_maxUnambigiousRange(radar)
    radar['RF_AnalogNoiseFilter_Bandwidth_MHz']=20
    radar['DopplerProcessingMIMODemod']='Simple'
    radar['ADC_levels']=256*8
    radar['RangeFFT_OverNextP2']=1
    radar['DopplerFFT_OverNextP2']=0
    radar['AzFFT_OverNextP2']=5
    # radar['NPulse']=12
    
# specifications['RangeFFT_OverNextP2'] = radarobject['GeneralRadarSpec_Object']['RangeFFT_OverNextP2']
# specifications['DopplerFFT_OverNextP2'] = radarobject['GeneralRadarSpec_Object']['']
# specifications['AzFFT_OverNextP2'] = radarobject['GeneralRadarSpec_Object']['AzFFT_OverNextP2']
# specifications['ElFFT_OverNextP2'] = radarobject['GeneralRadarSpec_Object']['ElFFT_OverNextP2']

    ssp.utils.set_frame_start_end(start=1,end=40)
    ssp.utils.useCUDA()
    ssp.utils.trimUserInputs() 
    ssp.config.restart()
    ssp.config.DopplerProcessingMethod_FFT_Winv = (True)

    ssp.config.directReceivefromTX =  False 
    ssp.config.RadarRX_only_fromscatters_itsTX = True
    ssp.config.RadarRX_only_fromitsTX = True
    ssp.config.Radar_TX_RX_isolation = True
    ssp.utils.save_Blender()


def processing_1():
    ssp.utils.trimUserInputs() 
    ssp.config.restart()
    ssp.config.setDopplerProcessingMethod_FFT_Winv(0)
    # plt.ion() 
    fig, FigsAxes = plt.subplots(2,3)
    FigsAxes[1, 2] = fig.add_subplot(2, 3, 6, projection='3d')
    while ssp.config.run():
        path_d_drate_amp = ssp.raytracing.Path_RayTracing_frame()
        alld = []
        m = path_d_drate_amp[0][0][0][0][0][0][0][3]
        for itx in range(len(path_d_drate_amp[0][0][0][0][0])):
            for irx in range(len(path_d_drate_amp[0][0])):
                for d_drate_amp in path_d_drate_amp[0][0][irx][0][0][itx]:
                    # if d_drate_amp[3]==m:
                    alld.append(d_drate_amp[0:3])
        alld = np.array(alld)
        fig.suptitle(f'Frame: {ssp.config.CurrentFrame}')
        FigsAxes[0,2].cla()
        # FigsAxes[1,2].cla()
        # FigsAxes[0,2].plot(alld[:,0],'.')
        # FigsAxes[1,2].plot(alld[:,1],'.')
        # FigsAxes[0,2].set_xlabel('scatter index')
        # FigsAxes[0,2].set_ylabel('d (m)')
        # FigsAxes[1,2].set_xlabel('scatter index')
        # FigsAxes[1,2].set_ylabel('dr (m/s)')
    
        # ssp.utils.force_zeroDoppler_4Simulation(path_d_drate_amp)
        Signals = ssp.integratedSensorSuite.SensorsSignalGeneration_frame(path_d_drate_amp)
        ssp.integratedSensorSuite.SensorsSignalProccessing_Chain_RangeProfile_RangeDoppler_AngleDoppler(Signals,FigsAxes,fig)
        ssp.utils.increaseCurrentFrame()
    # plt.ioff() 
    plt.show()
    
def processing_4():
    ssp.utils.trimUserInputs() 
    ssp.config.restart()
    fig, FigsAxes = plt.subplots(2,2)
    # FigsAxes[1] = fig.add_subplot(1, 2, 2, projection='3d')
    while ssp.config.run():
        path_d_drate_amp = ssp.raytracing.Path_RayTracing_frame()
        fig.suptitle(f'Frame: {ssp.config.CurrentFrame}')
        Signals = ssp.integratedSensorSuite.SensorsSignalGeneration_frame(path_d_drate_amp)
        ssp.integratedSensorSuite.SensorsSignalProccessing_Chain_RangeProfile_RangeDoppler_AngleDoppler_TruckHuman_Detection(Signals,FigsAxes,fig)
        ssp.utils.increaseCurrentFrame()
        print(f'Frame: {ssp.config.CurrentFrame}')
    # plt.ioff() 
    plt.show()

def processing_3():
    ssp.utils.trimUserInputs() 
    ssp.config.restart()
    fig, FigsAxes = plt.subplots(1,2)
    # FigsAxes[1] = fig.add_subplot(1, 2, 2, projection='3d')
    while ssp.config.run():
        path_d_drate_amp = ssp.raytracing.Path_RayTracing_frame()
        # fig2, FigsAxes2 = plt.subplots(len(ssp.lastSuite_Position[0]['Radar'][0]['TX-Position']),
        #                                len(ssp.lastSuite_Position[0]['Radar'][0]['RX-Position']))
        # for itx in range(len(ssp.lastSuite_Position[0]['Radar'][0]['TX-Position'])):
        #     for irx in range(len(ssp.lastSuite_Position[0]['Radar'][0]['RX-Position'])):
        #         print("Test",ssp.config.CurrentFrame,itx,irx,(path_d_drate_amp[0][0][irx][0][0][itx]))
        #         if itx+irx==0:
        #             FigsAxes2[itx,irx].plot([x[0] for x in path_d_drate_amp[0][0][irx][0][0][itx]],[x[2] for x in path_d_drate_amp[0][0][irx][0][0][itx]],'.')
        #         else:
        #             FigsAxes2[itx,irx].plot([x[0] for x in path_d_drate_amp[0][0][irx][0][0][itx]],[x[2] for x in path_d_drate_amp[0][0][irx][0][0][itx]],'.')
        # plt.show()
        fig.suptitle(f'Frame: {ssp.config.CurrentFrame}')
        # FigsAxes[0,2].cla()
        Signals = ssp.integratedSensorSuite.SensorsSignalGeneration_frame(path_d_drate_amp)
        ssp.integratedSensorSuite.SensorsSignalProccessing_Chain_RangeProfile_RangeDoppler_AngleDoppler_TruckHuman(Signals,FigsAxes,fig)
        ssp.utils.increaseCurrentFrame()
        print(f'Frame: {ssp.config.CurrentFrame}')
    # plt.ioff() 
    plt.show()
    
def processing_2():
    ssp.utils.trimUserInputs() 
    ssp.config.restart()
    ssp.config.setDopplerProcessingMethod_FFT_Winv(1)
    fig, FigsAxes = plt.subplots(2,3)
    while ssp.config.run():
        path_d_drate_amp = ssp.raytracing.Path_RayTracing_frame()
        # ssp.utils.force_zeroDoppler_4Simulation(path_d_drate_amp)
        # Channel_d_fd_amp = ssp.visualization.visualize_radar_path_d_drate_amp(path_d_drate_amp,1)
        radar_path_d_drate_amp(path_d_drate_amp,[fig,FigsAxes])
        ssp.utils.increaseCurrentFrame()
    # plt.show()
    

def radar_path_d_drate_amp(path_d_drate_amp,FigsAxes):
    alld = []
    m = path_d_drate_amp[0][0][0][0][0][0][0][3]
    for itx in range(len(path_d_drate_amp[0][0][0][0][0])):
        for irx in range(len(path_d_drate_amp[0][0])):
            for d_drate_amp in path_d_drate_amp[0][0][irx][0][0][itx]:
                if d_drate_amp[3]==m:
                    alld.append(d_drate_amp[0:3])
    alld = np.array(alld)
    FigsAxes[1][0,0].plot(alld[:,0])
    FigsAxes[1][0,1].plot(alld[:,1])
    FigsAxes[1][1,0].plot(alld[:,2])
    FigsAxes[1][1,1].plot(np.diff(alld[:,0]))
    FigsAxes[1][1,2].plot(np.diff(np.diff(alld[:,0])))
    image=ssp.visualization.captureFig(FigsAxes[0])
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    cv2.imshow('d drate ', image)
    if cv2.waitKey(50) & 0xFF == ord('q'):
        return

    
    # plt.draw() 
    # plt.pause(0.1)


def raytracing_test():
    ssp.utils.trimUserInputs() 
    ssp.config.restart()
    ssp.config.RayTracing_ReflectionPointEpsilon=1e-4
    empty_obj = bpy.data.objects.get("Plot Rays")
    if empty_obj:
        # Collect all children recursively
        def collect_children_recursive(obj):
            children = list(obj.children)
            for child in obj.children:
                children.extend(collect_children_recursive(child))
            return children

        # Get all descendants of the empty
        descendants = collect_children_recursive(empty_obj)

        # Deselect all objects first
        bpy.ops.object.select_all(action='DESELECT')

        # Select the empty and all its descendants
        empty_obj.select_set(True)
        for child in descendants:
            child.select_set(True)

        # Delete the selected objects
        bpy.ops.object.delete()
    
    bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD', location=(0, 0, 0), rotation=(0, 0, 0), scale=(1, 1, 1))
    allrays = bpy.context.object
    allrays.name = f'Plot Rays'
    while ssp.config.run():    
        bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD', location=(0, 0, 0), rotation=(0, 0, 0), scale=(1, 1, 1))
        framerays = bpy.context.object
        framerays.name = f'Plot Rays Frame {ssp.config.getCurrentFrame()}'
        framerays.parent=allrays 
        path_d_drate_amp = ssp.raytracing.Path_RayTracing_frame()
        path_index = 1
        for isrx,suiteRX_d_drate_amp in path_d_drate_amp.items():
            for irrx,radarRX_d_drate_amp in suiteRX_d_drate_amp.items():
                for irx,RX_d_drate_amp in radarRX_d_drate_amp.items():
                    for istx,suiteTX_d_drate_amp in RX_d_drate_amp.items():
                        for irtx,radarTX_d_drate_amp in suiteTX_d_drate_amp.items():
                            for itx,TX_d_drate_amp in radarTX_d_drate_amp.items():
                                for ip,p in enumerate(TX_d_drate_amp):
                                    d,dr,a,m=p
                                    print(path_index,len(m),m,d)
                                    tx = ssp.lastSuite_Position[istx]['Radar'][irtx]['TX-Position'][itx] 
                                    rx = ssp.lastSuite_Position[isrx]['Radar'][irrx]['RX-Position'][irx]
                                    v = [tx]
                                    for mi in m:
                                        if isinstance(mi, list) and len(mi) == 2 and isinstance(mi[1], Vector):
                                            v.append(mi[1])
                                        if isinstance(mi, str):
                                            _, is0, ir0, iris0 = mi.split('_')
                                            is0 = int(is0)
                                            ir0 = int(ir0)
                                            iris0 = int(iris0)
                                            v.append(ssp.lastSuite_Position[is0]['RIS'][ir0]['Position'][iris0])
                                    v.append(rx)
                                    ray = ssp.visualization.plot_continuous_curve(v,framerays,curve_name=f'path {path_index} Frame {ssp.config.CurrentFrame}')
                                    ray["Ray Tracing 20log Amp (dB)"]=float(20*np.log10(a))
                                    ray["Ray Tracing distance"]=float(d)
                                    ray["Ray Tracing doppler * f0"]=float(dr)
                                    ray["Middle Number"]=len(m)
                                    path_index+=1
                                    
        ssp.utils.increaseCurrentFrame()
        break

