import os
import sys
import struct
import array
import binascii


cvs = open(sys.argv[1].replace(".ply",".csv"), "w")

class poly(object):
        def __init__(self,name = ""):
                self.name = name
                self.verts = []
                self.normals = []
                self.color = []
                self.uv0 = []
                self.faces = []

for xyz in range(1,len(sys.argv)):
        smd = open(sys.argv[xyz], "r")

        pol = poly()
        Mode = 0
        vertCount = 0
        curCountV = 0
        faceCount = 0
        curCountF = 0
        for line in smd:
                
                if line.startswith("element"):
                        if line.split(" ")[1] == "vertex":
                                vertCount = int(line.split(" ")[2])
                        if line.split(" ")[1] == "face":
                                faceCount = int(line.split(" ")[2])
                elif line.startswith("end_header"):
                        Mode = 1
                elif Mode == 1:
                        if curCountV < vertCount:
                                rLine = line.split()

                                if len(rLine) >= 12: # xyz + nx ny nz + RGBA + UV
                                        # POSITION
                                        pol.verts.append([rLine[0], rLine[1], rLine[2]])

                                        # NORMALS
                                        pol.normals.append([rLine[3], rLine[4], rLine[5]])

                                        # COLOR RGBA
                                        pol.color.append([rLine[6], rLine[7], rLine[8], rLine[9]])

                                        # UV
                                        pol.uv0.append([rLine[10], rLine[11]])

                                elif len(rLine) == 10: # xyz + nx ny nz + RGBA (no UV)
                                        print("xyz + nx ny nz + RGBA (no UV):", rLine)

                                        # POSITION
                                        pol.verts.append([rLine[0], rLine[1], rLine[2]])

                                        # NORMALS
                                        pol.normals.append([rLine[3], rLine[4], rLine[5]])

                                        # COLOR RGBA
                                        pol.color.append([rLine[6], rLine[7], rLine[8], rLine[9]])
                                        
                                        # UV fallback
                                        pol.uv0.append([0.0, 0.0])

                                elif len(rLine) == 9: # xyz + RGBA + UV (no normals?)
                                        print("xyz + RGBA + UV (no normals?):", rLine)

                                        # POSITION
                                        pol.verts.append([rLine[0], rLine[1], rLine[2]])

                                        # NORMALS fallback
                                        pol.normals.append([0.0, 0.0, 1.0])

                                        # COLOR RGBA
                                        pol.color.append([rLine[3], rLine[4], rLine[5], rLine[6]])

                                        # UV
                                        pol.uv0.append([rLine[7], rLine[8]])

                                elif len(rLine) == 8: # xyz + nx ny nz + UV (no color)
                                        print("xyz + nx ny nz + UV (no color):", rLine)
                                        
                                        # POSITION
                                        pol.verts.append([rLine[0], rLine[1], rLine[2]])

                                        # NORMALS
                                        pol.normals.append([rLine[3], rLine[4], rLine[5]])

                                        # COLOR RGBA fallback
                                        pol.color.append([255, 255, 255, 255])

                                        # UV
                                        pol.uv0.append([rLine[6], rLine[7]])

                                elif len(rLine) == 6: # xyz + nx ny nz (no colors, no uv)
                                        print("xyz + nx ny nz (no colors, no uv):", rLine)

                                        # POSITION
                                        pol.verts.append([rLine[0], rLine[1], rLine[2]])

                                        # NORMALS (REAL, not fallback)
                                        pol.normals.append([rLine[3], rLine[4], rLine[5]])

                                        # COLOR RGBA fallback
                                        pol.color.append([255, 255, 255, 255])

                                        # UV fallback
                                        pol.uv0.append([0.0, 0.0])

                                elif len(rLine) == 3: # (position only)
                                        print("(position only):", rLine)

                                        # POSITION
                                        pol.verts.append([rLine[0], rLine[1], rLine[2]])

                                        pol.normals.append([0.0, 0.0, 1.0])
                                        pol.color.append([255, 255, 255, 255])
                                        pol.uv0.append([0.0, 0.0])

                                else:
                                        print("INVALID VERTEX LINE:", rLine)

                                        # safe fallback so pipeline doesn't crash
                                        pol.verts.append([0.0, 0.0, 0.0])
                                        pol.normals.append([0.0, 0.0, 1.0])
                                        pol.color.append([255, 255, 255, 255])
                                        pol.uv0.append([0.0, 0.0])

                                curCountV += 1

                        elif curCountF < faceCount:
                                rLine = line.split()
                                rLine.pop(0)
                                pol.faces.append(rLine)
                                curCountF+=1
                        else:
                                pass
                else:
                        pass



        obj = pol
        obj_name = os.path.basename(sys.argv[xyz]).replace(".ply","")
        cvs.write("Obj Name:%s\nUV_Num:1\nvert_Array\n" % obj_name)
        for idx,v in enumerate(obj.verts):
                n = obj.normals[idx]
                u = obj.uv0[idx]
                c = obj.color[idx]
                cvs.write(str("%s,%s,%s\n" % (v[0],v[1],v[2])))
                cvs.write(str("%s,%s,%s\n" % (n[0],n[1],n[2])))
                cvs.write(str("%s,%s,%s,%s\n" % (c[0],c[1],c[2],c[3])))#GB
                cvs.write(str("%s,%s\n" % (u[0],u[1])))
        cvs.write(str("face_Array\n"))
        for f in obj.faces:
                cvs.write(str("%i,%i,%i\n" % (int(f[0])+1,int(f[1])+1,int(f[2])+1)))

