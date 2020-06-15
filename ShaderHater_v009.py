# Welcome to Shader Hater, the script for those whose hate manually building shader networks

# The easiest way to use this script is to directly drop it into Maya 

# Select a directory of shader images 
# this works best if materials are separated into different folders. 

# Change the name if desired (You'll probable want to) 
# Check that all Images were found
# Choose render engine and Create! 

# Please reach out if there are any questions, concerns or feedback rine.of.harts@gmail.com
# NOTE: I am not a programmer! Let me know if there is anything I can do to make this tool better in the future.

import maya.cmds as cmds
import mtoa.core as mtoa
from functools import partial
import os 


def UI(): 
	
	icon = cmds.internalVar(upd = True) + "/fileOpen.png"

	if cmds.window ("ShaderHater", exists = True):
		cmds.deleteUI("ShaderHater")

	filePromptWindow = cmds.window("ShaderHater", sizeable = True, title = "Shader Hater", widthHeight = (410,	750	))
	
	# Main Column Layout
	mainLayout = cmds.columnLayout( w = 410 , h = 750 , cal = 'center' )

	#Row Layout
	cmds.separator(height = 10)
	fileColumLayout = cmds.rowColumnLayout(numberOfColumns = 2, cal = [(1, 'center'),(2, 'center')], columnWidth = [(1,360),(2,40)],
										   columnOffset = [(1,'left',10),(2,'both',10)])
	#Input Fields
	cmds.separator(height = 10, style = "none")
	cmds.separator(height = 10, style = "none")

	cmds.text( label='Material Name', align = "left")
	cmds.text( label='')

	cmds.textField("texName", width = 360, height = 30)
	cmds.text( label='')

	cmds.separator(height = 10, style = "none")
	cmds.separator(height = 10, style = "none")
	
	cmds.text( label='Select Shader Directory', align = "left")
	cmds.text( label='')
	
	cmds.textField("ShaderDirectory" , width = 360)
	cmds.symbolButton("sd_Btn", w = 30, h = 30, image = icon, command = partial(selectByDirectory, 'ShaderDirectory'))

	cmds.separator(height = 10, style = "none")
	cmds.separator(height = 10, style = "none")	

	cmds.checkBox("udimCB", label = 'Include UDIM')
	cmds.text( label = '')

	cmds.checkBox( "indivFilesCB", label = 'Select Individual Files', onCommand = partial(enableDisableIndivSelect , 1), offCommand = partial(enableDisableIndivSelect ,0))
	cmds.text( label = '')

	cmds.separator(height = 10, style = "none")
	cmds.separator(height = 10, style = "none")	

	cmds.text( label='Base Color / Diffuse', align = "left")
	cmds.text( label='')
	
	cmds.textField("BaseColor" , width = 360, enable = False)
	cmds.symbolButton("bc_Btn", enable = False, w = 30, h = 30, image = icon, command = partial(selectIndivFiles, "BaseColor"))

	cmds.separator(height = 10, style = "none")
	cmds.separator(height = 10, style = "none")

	cmds.text( label='Metalness / Spec', align = "left")
	cmds.text( label='')

	cmds.textField("Metalness", width = 360, enable = False)
	cmds.symbolButton("metal_Btn", enable = False, w = 30, h = 30, image = icon, command = partial(selectIndivFiles, "Metalness"))

	cmds.separator(height = 10, style = "none")
	cmds.separator(height = 10, style = "none")

	
	cmds.text( label='Roughness', align = "left")
	cmds.text( label='')

	cmds.textField("Roughness", width = 360, enable = False)
	cmds.symbolButton("rough_Btn", enable = False, w = 30, h = 30, image = icon, command = partial(selectIndivFiles, "Roughness"))

	cmds.separator(height = 10, style = "none")
	cmds.separator(height = 10, style = "none")

	cmds.text( label='Normal', align = "left")
	cmds.text( label='')

	cmds.textField("Normal", width = 360, enable = False)
	cmds.symbolButton("norm_Btn", enable = False, w = 30, h = 30, image = icon, command = partial(selectIndivFiles, "Normal"))

	cmds.separator(height = 10, style = "none")
	cmds.separator(height = 10, style = "none")

	cmds.text( label='Height / Displacement', align = "left")
	cmds.text( label='')

	cmds.textField("Height", width = 360, enable = False)
	cmds.symbolButton("height_Btn", enable = False, w = 30, h = 30, image = icon, command = partial(selectIndivFiles, "Height")) 

	cmds.separator(height = 10, style = "none")
	cmds.separator(height = 10, style = "none")

	cmds.text( label='AO', align = "left")
	cmds.text( label='')

	cmds.textField("AO", width = 360, enable = False)
	cmds.symbolButton("ao_Btn", enable = False, w = 30, h = 30, image = icon, command = partial(selectIndivFiles, "AO"))

	cmds.separator(height = 10, style = "none")
	cmds.separator(height = 10, style = "none")

	cmds.text( label='Emissive', align = "left")
	cmds.text( label='')

	cmds.textField("Emissive", width = 360, enable = False)
	cmds.symbolButton("trans_Btn", enable = False, w = 30, h = 30, image = icon, command = partial(selectIndivFiles, "Emissive"))

	cmds.separator(height = 10, style = "none")
	cmds.separator(height = 10, style = "none")

	cmds.text( label='Opacity', align = "left")
	cmds.text( label='')

	cmds.textField("Opacity", width = 360, enable = False)
	cmds.symbolButton("opac_Btn", enable = False, w = 30, h = 30, image = icon, command = partial(selectIndivFiles, "Opacity"))

	btnColumLayout = cmds.rowColumnLayout(numberOfColumns = 2, columnWidth = [(1,200),(2,200)], columnOffset = [(1,'both',20),(2,'both',20)], parent = mainLayout)
	cmds.separator(height = 15, style = "none")
	cmds.separator(height = 15, style = "none")

	cmds.checkBox( "arnoldSelectCB", label = 'Arnold Material', value = True, onCommand = partial ( renderSelectCheck , 0 ), offCommand = partial ( renderSelectCheck , 1 ))
	cmds.checkBox( "redshiftSelectCB", label = 'Redshift Material', value = False, onCommand = partial ( renderSelectCheck , 1 ), offCommand = partial ( renderSelectCheck , 0 ))

	cmds.separator(height = 25, style = "none")
	cmds.separator(height = 25, style = "none")
	
	cmds.button(w = 160 , h = 30, label = "Create", parent = btnColumLayout , c = partial(hateTheShader))
	cmds.button(w = 160 , h = 30, label = "Cancel", parent = btnColumLayout, c = ('cmds.deleteUI(\"' + filePromptWindow + '\", window=True)'))

	cmds.showWindow ( filePromptWindow )

#Query the contents or states of the textFields/ CheckBoxes 
def queryEditFields(*args): 
	queryList = []
	newFieldList = []
	for field in txtFieldList:
		newFieldList.append(field) 
		queryField = cmds.textField(field, q = True, tx = True )
		if queryField != '' :
			queryList.append(queryField)
		if queryField == '':
			newFieldList.remove(field)
	return queryList, newFieldList

# Open fileDialog to select directory NOT files 
# Read img files in dir and propulate textfields appropriately
# Must search for all possible variations of texture names
# Set Shader name based on dir
def selectByDirectory(textField, *args):

	oldCheck = queryEditFields()[0]
	if len(oldCheck) > 0 : 
		for field in txtFieldList: 
			cmds.textField(field, e = True, tx = '' )

	udimCheck = cmds.checkBox("udimCB", q = True, v = True)
	inputDirectory = cmds.fileDialog2(fileMode = 2, ds = 2, okc = 'Okay', cc = "Never!" )[0]
	shaderFiles = os.listdir(inputDirectory)
	shaderFiles = [ file for file in shaderFiles if file.endswith( 
	('.bmp', '.ico', '.jpeg', '.jpg', '.jng', '.pbm', '.pgm', '.ppm', '.png','.targa', '.tiff',
	'.wbmp', '.xpm', '.gif', '.hdr', '.exr', '.j2k', '.jpeg-2000', '.pfm', '.psd'))]
	
	bcList = ['BaseColor', 'basecolor', 'diff', 'bc', 'Diffuse']
	metalList = ['Metalness', 'metal', 'reflect', 'Reflectiv', 'Metal']
	roughList = ['Roughness', 'roughness', 'rough']
	normList = ['Normal', 'normal', 'Nor', 'nor']
	heightList = ['Height', 'height', 'disp', 'displacement']
	ambientList = ['AO', 'ambient', 'Ambient']
	emissList = ['Emissive', 'emiss']
	opacList = ['Opacity', 'opac', 'transpar', 'Trans']

	if udimCheck == True: 
			shaderFiles = [ file for file in shaderFiles if '1001' in file]
			print shaderFiles

	for name in shaderFiles:
	
		if any(x in name for x in bcList):
			cmds.textField('BaseColor', edit = True, tx = name)

		elif any(x in name for x in metalList):
			cmds.textField('Metalness', edit = True, tx = name)
		
		elif any(x in name for x in roughList):
			cmds.textField('Roughness', edit = True, tx = name)
		
		elif any(x in name for x in normList):
			cmds.textField('Normal', edit = True, tx = name)

		elif any(x in name for x in heightList):
			cmds.textField('Height', edit = True, tx = name)

		elif any(x in name for x in ambientList):
			cmds.textField('AO', edit = True, tx = name)

		elif any(x in name for x in emissList):
			cmds.textField('Emissive', edit = True, tx = name)

		elif any(x in name for x in opacList):
			cmds.textField('Opacity', edit = True, tx = name)
		

	cmds.textField(textField, edit = True, text = inputDirectory )
	inputName = inputDirectory.split("/")[-1]
	texName = cmds.textField("texName", q = True, text = True)
	if texName == "": 
		cmds.textField("texName", edit = True, text = inputName)
	elif texName != inputName: 
		cmds.textField("texName", edit = True, text = inputName)


def selectIndivFiles(textField, *args): 

	FilePath = cmds.fileDialog2(fileFilter = multipleFilters, selectFileFilter = '.png (*.png)', fileMode = 1, ds = 2, okc = 'Okay', cc = "Never!" )[0]
	cmds.textField( textField, edit = True, text = FilePath )

def buildShaderLists(): 

	fullShaderPath = []
	shaderNameOnly = []
	inputShaderFiles = queryEditFields()[0]
	inputDir = cmds.textField('ShaderDirectory', q = True, tx = True)

	for file in inputShaderFiles: 
		fullShaderPath.append(inputDir + '/' + file)
		shaderNameOnly.append(os.path.splitext(file)[0])

	return fullShaderPath, shaderNameOnly, inputShaderFiles


def hateTheShader(*args):

	texName = cmds.textField("texName", q = True, text = True)
	checkUdimBox = cmds.checkBox('udimCB', q = True, value = True)
	checkArnoldBox = cmds.checkBox('arnoldSelectCB', q = True, value = True)
	checkRedshiftBox = cmds.checkBox('redshiftSelectCB', q = True, value = True)
	textureList = (buildShaderLists()[1])
	textureList_with_ext =(buildShaderLists()[2])
	fullShaderFile_path = buildShaderLists()[0]
	currentTxtFieldList = (queryEditFields()[1])
	newTexList = []
	fileNodeList = []
	place2dtextureList = []

	print currentTxtFieldList, len(currentTxtFieldList)
	print textureList , len(textureList)
	print fullShaderFile_path , len(fullShaderFile_path)
	# Duplicate Name Check
	matList = cmds.ls(mat = True)
	for name in matList: 
		if name == texName: 
			cmds.confirmDialog( title = 'ERROR', message = 'Cannot have duplicate shader name' )
			cmds.error( 'Cannot create shader with duplicate name')
	
	if texName == '' and checkRedshiftBox == True:
		texName = 'rsMaterial1'
	
	# Duplicate Image Check		
	textureCheckList = cmds.ls( type = 'file')
	for shad in textureList: 
		if shad in textureCheckList:
			cmds.confirmDialog( title = 'ERROR', message = 'Please select new image files or Duplicate Graph' )
			cmds.error( 'Cannot create 2 shaders with duplicate image files')
				
	textureNodeNames= []

	for each in textureList:
		textureNodeNames = [s.replace('.', '_') for s in textureList]

	for x in textureNodeNames:
		textureNode = cmds.shadingNode("file", asTexture = True, name = x)
		placed2dTextureNode = cmds.shadingNode("place2dTexture", asUtility = True, name = texName +"place2dTexture1")
		newTexList.append(x)
		fileNodeList.append(textureNode)
		place2dtextureList.append(placed2dTextureNode)
	
	placed2dTextureConnections = ['rotateUV','offset','noiseUV','vertexCameraOne','vertexUvThree','vertexUvTwo','vertexUvOne',
								  'repeatUV','wrapV','wrapU','stagger','mirrorU','mirrorV','rotateFrame','translateFrame','coverage']

	for tex in range(len(place2dtextureList)):			
	    cmds.connectAttr(place2dtextureList[tex] + '.outUV', newTexList[tex] + '.uvCoord')
	    cmds.connectAttr(place2dtextureList[tex] + '.outUvFilterSize', newTexList[tex] + '.uvFilterSize')
	    for connection in placed2dTextureConnections:
	        cmds.connectAttr(place2dtextureList[tex] + '.' + connection, newTexList[tex] + '.' + connection)
	
	for t in range(len(fileNodeList)):
		cmds.setAttr(fileNodeList[t]+ '.fileTextureName', fullShaderFile_path[t], type = "string")

	if checkUdimBox == True: 
		for t in range(len(fileNodeList)):
			cmds.setAttr(fileNodeList[t]+ '.uvTilingMode', 3 )
	        
	if checkArnoldBox == True:
		mtoa.createArnoldNode ('aiStandardSurface', name = texName, skipSelect = False, runtimeClassification = None)
	
		#Connecting Textures to Corresponding Shader Attribute
		for ff in range (len(currentTxtFieldList)): 
			
			if currentTxtFieldList[ff] == "BaseColor":
				cmds.connectAttr(textureNodeNames[ff] + '.outColor', texName + '.baseColor', force = 1)
			
			elif  currentTxtFieldList[ff] == "Metalness":
				cmds.connectAttr(textureNodeNames[ff] + '.outColorR', texName + '.metalness', force = 1)
				cmds.setAttr(textureNodeNames[ff] + '.colorSpace', 'Raw', type = "string")
			
			elif currentTxtFieldList[ff] == 'Roughness':
				cmds.connectAttr(textureNodeNames[ff] + '.outColorR', texName + '.specularRoughness', force = 1)
				cmds.setAttr(textureNodeNames[ff] + '.colorSpace', 'Raw', type = "string")
			
			elif currentTxtFieldList[ff] == "Normal" :
				mtoa.createArnoldNode('aiNormalMap', name = textureNodeNames[ff] + "_Normal", skipSelect = False, runtimeClassification = None)
				cmds.connectAttr(textureNodeNames[ff] + '_Normal.outValue', texName + '.normalCamera', force = 1)
				cmds.connectAttr(textureNodeNames[ff] + '.outColor', textureNodeNames[ff] + '_Normal.input', force = 1)
				cmds.setAttr(textureNodeNames[ff] + '.colorSpace', 'Raw', type = "string")
			
			elif currentTxtFieldList[ff] == "Emissive":
				cmds.connectAttr(textureNodeNames[ff] + '.outColor', texName + '.emissionColor', force = 1)
			
			elif currentTxtFieldList[ff] == "Opacity" :
				cmds.shadingNode("reverse", asUtility = True)
				cmds.connectAttr('reverse1.outputX', texName + '.transmission', force = 1)
				cmds.connectAttr(textureNodeNames[ff] + '.outColor', 'reverse1.input', force = 1)
				cmds.setAttr(textureNodeNames[ff] + '.colorSpace', 'Raw', type = "string")
			
			elif  currentTxtFieldList[ff] == "Height" :
				cmds.shadingNode("displacementShader", name = textureNodeNames[ff] + '_Displace', asShader = True)
				cmds.connectAttr(textureNodeNames[ff] + '.outColorR', textureNodeNames[ff] + '_Displace.displacement', force = 1)
				cmds.setAttr(textureNodeNames[ff] + '.colorSpace', 'Raw', type = "string")
				cmds.connectAttr( textureNodeNames[ff] + '_Displace.displacement', texName + 'SG' + '.displacementShader')

	elif checkRedshiftBox == True: 
		cmds.shadingNode('RedshiftMaterial', asShader = True, name = texName)

		cmds.sets( renderable = True, noSurfaceShader = True, empty = True, name = texName + 'SG' )
		
		cmds.connectAttr( texName + '.outColor', texName + 'SG' + '.surfaceShader')
		cmds.setAttr(texName + '.refl_brdf', 1)
		cmds.setAttr( texName + '.refl_fresnel_mode', 2)
		for ff in range (len(currentTxtFieldList)):
			
			if currentTxtFieldList[ff] == "BaseColor":
				cmds.connectAttr(textureNodeNames[ff] + '.outColor', texName + '.diffuse_color', force= 1)
				cmds.setAttr(textureNodeNames[ff] + '.ignoreColorSpaceFileRules', 1)
			
			elif  currentTxtFieldList[ff] == "Metalness":
				cmds.connectAttr(textureNodeNames[ff] + '.outAlpha', texName + '.refl_metalness', force= 1)
				cmds.setAttr(textureNodeNames[ff] + '.colorSpace', 'Raw', type = "string")
				cmds.setAttr(textureNodeNames[ff] + '.ignoreColorSpaceFileRules', 1)
			
			elif currentTxtFieldList[ff] == 'Roughness':
				cmds.connectAttr(textureNodeNames[ff] + '.outAlpha', texName + '.refl_roughness', force= 1)
				cmds.setAttr(textureNodeNames[ff] + '.colorSpace', 'Raw', type = "string")
				cmds.setAttr(textureNodeNames[ff] + '.alphaIsLuminance', 1)
				cmds.setAttr(textureNodeNames[ff] + '.ignoreColorSpaceFileRules', 1)
			
			elif currentTxtFieldList[ff] == 'Normal':
				cmds.shadingNode('RedshiftBumpMap', asTexture = True, name = textureNodeNames[ff] + "_NormalMap")
				cmds.connectAttr(textureNodeNames[ff] + '_NormalMap.out', texName + '.bump_input', force= 1)
				cmds.connectAttr(textureNodeNames[ff] + '.outColor', textureNodeNames[ff] + '_NormalMap.input', force= 1)
				cmds.setAttr(textureNodeNames[ff] + '.colorSpace', 'Raw', type = "string")
				cmds.setAttr(textureNodeNames[ff] + '.alphaIsLuminance', 1)
				cmds.setAttr(textureNodeNames[ff] + '.ignoreColorSpaceFileRules', 1)
				cmds.setAttr(textureNodeNames[ff] + "_NormalMap" + '.flipY', 1)
				cmds.setAttr(textureNodeNames[ff] + '_NormalMap' + '.inputType', 1)
				cmds.setAttr(textureNodeNames[ff] + '_NormalMap' + '.scale', 1)

			elif currentTxtFieldList[ff] == 'Emissive':
				cmds.connectAttr(textureNodeNames[ff] + '.outColor', texName + '.emission_color', force= 1)
				cmds.setAttr(textureNodeNames[ff] + '.ignoreColorSpaceFileRules', 1)
			
			elif currentTxtFieldList[ff] == 'Opacity':
				cmds.connectAttr(textureNodeNames[ff] + '.outColorR', texName + '.refr_weight', force= 1)
				cmds.setAttr(textureNodeNames[ff] + '.colorSpace', 'Raw', type = "string")
				cmds.setAttr(textureNodeNames[ff] + '.alphaIsLuminance', 1)
				cmds.setAttr(textureNodeNames[ff] + '.invert', 1)
				cmds.setAttr(textureNodeNames[ff] + '.ignoreColorSpaceFileRules', 1)
				cmds.setAttr(texName + '.refl_fresnel_mode', 3)
			
			elif currentTxtFieldList[ff] == 'Height':
				cmds.shadingNode("RedshiftDisplacement", name = textureNodeNames[ff] + '_Displace', asShader=True)
				cmds.connectAttr(textureNodeNames[ff] + '.outColor', textureNodeNames[ff] + '_Displace.texMap', force= 1)
				cmds.setAttr(textureNodeNames[ff] + '.colorSpace', 'Raw', type = "string")
				cmds.setAttr(textureNodeNames[ff] + '.alphaIsLuminance', 1)
				cmds.connectAttr( textureNodeNames[ff] + '_Displace.out', texName + 'SG' + '.displacementShader')
				cmds.setAttr(textureNodeNames[ff] + '.ignoreColorSpaceFileRules', 1)

			elif currentTxtFieldList[ff] == 'AO': 
				cmds.shadingNode("RedshiftAmbientOcclusion", name = textureNodeNames[ff] + '_AO', asShader = True)
				cmds.connectAttr(textureNodeNames[ff] + '.outColor', textureNodeNames[ff] + '_AO.bright', force = 1)
				cmds.connectAttr(textureNodeNames[ff] + '.outColor', textureNodeNames[ff] + '_AO.dark', force = 1)
				cmds.connectAttr( textureNodeNames[ff] + '_AO.outColor', texName + '.overall_color')
				cmds.setAttr(textureNodeNames[ff] + '.ignoreColorSpaceFileRules', 1)



	# Clear out processed shader files and reset dialog
	enableDisableIndivSelect(2)
	print 'Material successfully created'

def enableDisableIndivSelect(num,*args):
	btnList = ["bc_Btn", "rough_Btn", "metal_Btn", "norm_Btn", "opac_Btn", "trans_Btn", 'ao_Btn']
	
	if num == 1:
		for btn in btnList : 
			cmds.disable(btn , v = False)
		
		for shader in txtFieldList: 
			cmds.textField( shader , edit = True, enable = True)
		
		cmds.textField("ShaderDirectory", edit = True, enable = False)
		cmds.disable("sd_Btn", v = True)

	elif num == 0: #Disable Btns and Dialog
		for btn in btnList : 
			cmds.disable(btn , v = True)
		
		for shader in txtFieldList: 
			cmds.textField( shader , edit = True, enable = False) 
		
		cmds.textField("ShaderDirectory", edit = True, enable = True)
		cmds.disable("sd_Btn", v = False)

	elif num == 2: #Disable and clear Btns and Dialog
		for btn in btnList : 
			cmds.disable(btn , v = True)
		
		for shader in txtFieldList: 
			cmds.textField( shader , edit = True, text = "", enable = False) 

		cmds.textField("Height", edit = True, text = "", enable = False)	
		cmds.textField("ShaderDirectory", edit = True,text = "", enable = True)
		cmds.disable("sd_Btn", v = False)
		cmds.textField("texName", edit = True, text = "")
		cmds.checkBox("udimCB", edit = True, value = False)
		cmds.checkBox("indivFilesCB", edit = True, value = False)



def renderSelectCheck(num, *args):
	if num == 0 : 
		cmds.checkBox( "arnoldSelectCB", edit = True, value = True)
		cmds.checkBox( "redshiftSelectCB", edit = True , value = False)
	if num == 1 : 
		cmds.checkBox( "arnoldSelectCB", edit = True, value = False)
		cmds.checkBox( "redshiftSelectCB", edit = True , value = True)


txtFieldList = ['BaseColor', "Metalness", "Roughness", "Normal", "Emissive", "Opacity", "Height", "AO"]

multipleFilters= '.bmp (*.bmp);; .ico (*.ico);; .jpeg (*.jpeg);; .jng (*.jng);; .pbm (*.pbm);; .pgm (*.pgm);; .ppm (*.ppm);;\
					 .png (*.png);; .targa (*.targa);; .tiff (*.tiff);; .wbmp (*.wbmp);; .xpm (*.xpm);; .gif (*.gif);; .hdr (*.hdr);;\
					 .exr (*.exr);; .j2k (*.j2k);; .jpeg-2000 (*.jpeg-2000);; .pfm (*.pfm);; .psd (*.psd);;'

UI()