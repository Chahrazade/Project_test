import bpy
import mathutils

#blablabla
#Get Point and Skull Meshes
flag1 = False 
flag2 = False

for object in bpy.context.scene.objects :
    if (object.name == "Skull") or (object.name == "skull") :
        skull = object.data
        flag1 = True
    if object.name == "Point"  or (object.name == "point") :
        point = object.data
        flag2 = True
            

if flag1 and flag2 :

    #Create a "blank" UVmap necessary to calc_tangents function
    uv_tex = skull.uv_textures.new()
    uv_layer = skull.uv_layers[-1]

    skull.calc_tangents(uv_layer.name)

    #Vertices selected in the mesh
    selected_idx = [i.index for i in skull.vertices if i.select]

    #Dictionary where key is vertex index and value is 
    #  (sum of tangent vectors, number of faces connected to the vertex)
    dic = {}

    point = mathutils.Vector((0,0,1))

    for l in skull.loops:
        if l.vertex_index in selected_idx :
            
            #Define tangent space
            planeNormal = mathutils.Vector.cross(l.tangent, l.bitangent)
            planePoint = skull.vertices[l.vertex_index].co
            
            #project point on the plane
            vec = point-planePoint
            signedDistance = mathutils.Vector.dot(planeNormal, vec)
            projectedPoint = point - (planeNormal * signedDistance)
            tgt_vec = projectedPoint-planePoint
            
            d = (-1)* mathutils.Vector.dot(planeNormal,planePoint)
            calc = r(mathutils.Vector.dot(planeNormal, projectedPoint) + d)
            print("Value : "+ str(calc))
            
            if l.vertex_index in dic :
                tmp = dic[l.vertex_index]
                dic[l.vertex_index] = tmp[0] + tgt_vec,tmp[1]+1
            else:
                dic[l.vertex_index]= tgt_vec, 1            
            
            
	  r = lambda x: round(x, 6)
    for key in dic : 
        vec.normalize()
        print("Vector : "+str(vec))
        vec_round = mathutils.Vector((r(vec[0]), r(vec[1]), r(vec[2])))
        print("Vector rounded : "+str(vec_round))
        print("Number of faces : " + str(dic[key][1]))
        dic[key] = vec, dic[key][1]

else : 
    print("Mesh \"Point\" and/or \"Skull\" not found.")