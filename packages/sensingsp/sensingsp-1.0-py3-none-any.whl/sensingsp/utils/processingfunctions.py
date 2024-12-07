import bpy 
import sensingsp as ssp
# import sensingsp as ssp
import numpy as np
from mathutils import Vector
from matplotlib import pyplot as plt
import matplotlib.cm as cm

def processing_functions_run1():
  ssp.utils.set_frame_start_end(start=bpy.context.scene.frame_start,end=2+0*bpy.context.scene.frame_end)
  ssp.utils.trimUserInputs() # input from bpy and blender UI -> ssp.RadarSpecifications
  ssp.raytracing.Path_RayTracing() # input from bpy, output ssp.Paths
  
  ssp.config.setDopplerProcessingMethod_FFT_Winv(1)
  ssp.config.restart()
  while ssp.config.run():
      Signals = ssp.integratedSensorSuite.SensorsSignalGeneration() # input is ssp.Paths in ssp.CurrentFrame
      ProcessingOutputs = ssp.integratedSensorSuite.SensorsSignalProccessing(Signals)
      ssp.visualization.visualizeProcessingOutputs(ProcessingOutputs)
      ssp.utils.saveMatFile(ProcessingOutputs)
      ssp.utils.increaseCurrentFrame()



def processing_functions_run2_old():
    ssp.utils.trimUserInputs() 
    ssp.raytracing.Path_RayTracing() 
    ssp.config.restart()
    ssp.config.define_axes(1)
    ssp.config.setDopplerProcessingMethod_FFT_Winv(1)
    while ssp.config.run():
        Signals = ssp.integratedSensorSuite.SensorsSignalGeneration() # input is ssp.Paths in ssp.CurrentFrame
        ssp.integratedSensorSuite.SensorsSignalProccessing_Angle(Signals)
        ssp.utils.increaseCurrentFrame()

def processing_functions_run2():
    ssp.utils.trimUserInputs() 
    ssp.config.restart()
    # ssp.config.define_axes(2)
    ssp.config.setDopplerProcessingMethod_FFT_Winv(1)
    while ssp.config.run():
        path_d_drate_amp = ssp.raytracing.Path_RayTracing_frame()
        Signals = ssp.integratedSensorSuite.SensorsSignalGeneration_frame(path_d_drate_amp)
        plt.plot(np.sin(np.arange(100)*.1))
        plt.pause(.1)
        # ssp.integratedSensorSuite.SensorsSignalProccessing_Angle_frame(Signals)
        # print(ssp.config.CurrentFrame)
        ssp.utils.increaseCurrentFrame()
    plt.show()
    
def processing_functions_run3():
    ssp.utils.trimUserInputs() 
    ssp.config.restart()
    ssp.config.define_axes()
    while ssp.config.run():
        ssp.raytracing.Path_RayTracing() 
        Signals = ssp.integratedSensorSuite.SensorsSignalGeneration() # input is ssp.Paths in ssp.CurrentFrame
        ssp.integratedSensorSuite.SensorsSignalProccessing_Angle(Signals)
        ssp.utils.increaseCurrentFrame()
    
def processing_functions_RISProbe1():
    db = True
    range_effect = True
    add_color = True
    add_open3d = True
    colormap = 'viridis' 
    size_scale = 0.05
    if "Simulation Settings" in bpy.data.objects:
        option = bpy.data.objects["Simulation Settings"]["Add Probe"]
        parts = option.split(',')
        db = str(parts[4])=='db1'
        range_effect = str(parts[5])=='range_effect1'
        add_color = str(parts[6])=='add_color1'
        add_open3d = str(parts[7])=='add_open3d1'
        if str(parts[8])=='colormap1':
            colormap = 'viridis'
        elif str(parts[8])=='colormap2':
            colormap = 'plasma'
        elif str(parts[8])=='colormap3':
            colormap = 'inferno'
        elif str(parts[8])=='colormap4':
            colormap = 'magma'
        elif str(parts[8])=='colormap5':
            colormap = 'jet'
        size_scale = float(parts[9])
    add_open3d = False
    
    ssp.utils.set_frame_start_end(start=1,end=2)
    ssp.utils.trimUserInputs() 
    ssp.config.restart()
    # Simple analysis for Probe (RIS)
    bpy.context.scene.frame_set(ssp.config.CurrentFrame)
    bpy.context.view_layer.update()
    depsgraph = bpy.context.evaluated_depsgraph_get()
    geocalculator = ssp.raytracing.BlenderGeometry()
    rayTracingFunctions = ssp.raytracing.RayTracingFunctions()
    suite_information = ssp.raytracing.BlenderSuiteFinder().find_suite_information()
    Suite_Position,ScattersGeo,HashFaceIndex_ScattersGeo,ScattersGeoV = geocalculator.get_Position_Velocity(bpy.context.scene, suite_information, ssp.config.CurrentFrame, 1)
    Lambda = 3e8 / 70e9
    sourcePos=Suite_Position[0]['Radar'][0]['TX-Position'][0]
    p1=ssp.raytracing.Vector3D(sourcePos.x,sourcePos.y,sourcePos.z)
    probe_values = []
    probe_xys = []
    for i in range(len(Suite_Position[0]['Probe'])):
        for probe_Pos in Suite_Position[0]['Probe'][i]:
            p3=ssp.raytracing.Vector3D(probe_Pos.x,probe_Pos.y,probe_Pos.z)
            o = 0
            for iriselement , ris_element_position in enumerate(Suite_Position[0]['RIS'][0]['Position']):
                p2=ssp.raytracing.Vector3D(ris_element_position.x,ris_element_position.y,ris_element_position.z)
                d1 = p2.distance_to(p1)
                d2 = p2.distance_to(p3)
                d=d1+d2
                phase = -2*np.pi*d / Lambda
                if range_effect:
                    amp = 1  / d1 / d2
                else:
                    amp = 1
                amp *= Suite_Position[0]['RIS'][0]['PhaseAmplitude'][iriselement][0]
                phase -= Suite_Position[0]['RIS'][0]['PhaseAmplitude'][iriselement][1]
                o += amp*np.exp(1j*phase)
            if db:
                probe_values.append(np.log10(np.abs(o)))
            else:
                probe_values.append(np.abs(o))
            probe_xys.append([probe_Pos.x,probe_Pos.y,probe_Pos.z])
    probe_xys = np.array(probe_xys)
    probe_values = np.array(probe_values)
    amplitudes_normalized = (probe_values - probe_values.min()) / (probe_values.max() - probe_values.min())
    amplitudes_normalized = .01+.99*amplitudes_normalized
    spheres = []
    
    bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD', location=(0, 0, 0), rotation=(0, 0, 0), scale=(1, 1, 1))
    empty = bpy.context.object
    empty.name = f'Probe Measurements'
    # empty = bpy.data.collections.new(f'Probe Measurements')
    # Create spheres based on the normalized amplitudes and probe positions
    
    for i in range(len(probe_xys)):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=amplitudes_normalized[i] * size_scale, location=(probe_xys[i][0],probe_xys[i][1],probe_xys[i][2]))
        sphere = bpy.context.object
        
        sphere.parent=empty
        if add_color:
            parula_colormap = cm.get_cmap(colormap)
            mat = bpy.data.materials.new(name="SphereMaterial")
            # mat.diffuse_color = (amplitudes_normalized[i], 0, 0, 1)  
            color = parula_colormap(amplitudes_normalized[i])[:3]  # Get RGB color from colormap
            mat.diffuse_color = (*color, 1)  # Set color based on amplitude
            sphere.data.materials.append(mat)

    if add_open3d:
        import open3d as o3d
        for i in range(len(probe_xys)):
            sphere = o3d.geometry.TriangleMesh.create_sphere(radius=amplitudes_normalized[i] * size_scale)
            sphere.translate(probe_xys[i])
            color = [amplitudes_normalized[i], 0, 0] 
            sphere.paint_uniform_color(color)
            spheres.append(sphere)
        combined_geometry = o3d.geometry.TriangleMesh()
        for sphere in spheres:
            combined_geometry += sphere
        o3d.visualization.draw_geometries([combined_geometry])
