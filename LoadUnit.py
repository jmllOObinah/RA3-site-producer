import os
import xml.etree.ElementTree as ET
CheckInheritFromList=["ArmorTemplate","LocomotorTemplate","WeaponTemplate","GameObject"]
def write_xml(tree, out_path):
    ET.register_namespace('','uri:ea.com:eala:asset')
    ET.register_namespace('xai','uri:ea.com:eala:asset:instance')
    ET.register_namespace('xsi','http://www.w3.org/2001/XMLSchema-instance')
    ET.register_namespace('xi','http://www.w3.org/2001/XInclude')
    node=ET.Element("meta-data")
    node.tail='\n\t'
    tree.write(out_path, encoding="utf-8",xml_declaration=True)
def prettyXml(element, indent, newline, level = 0): 
    # 判断element是否有子元素
    if element:
        # 如果element的text没有内容      
        if element.text == None or element.text.isspace():     
            element.text = newline + indent * (level + 1)      
        else:    
            element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * (level + 1)    
    # 此处两行如果把注释去掉，Element的text也会另起一行 
    #else:     
        #element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * level    
    temp = list(element) # 将elemnt转成list
    for subelement in temp:    
        # 如果不是list的最后一个元素，说明下一个行是同级别元素的起始，缩进应一致
        if temp.index(subelement) < (len(temp) - 1):     
            subelement.tail = newline + indent * (level + 1)    
        else:  # 如果是list的最后一个元素， 说明下一行是母元素的结束，缩进应该少一个    
            subelement.tail = newline + indent * (level + 1)
        # 对子元素进行递归操作 
        prettyXml(subelement, indent, newline, level = level)    
def mkdir(path):
    # 引入模块
    # 去除首位空格
    path=path.strip()
    # 去除尾部 \ 符号
    path=path.rstrip("\\")
 
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists=os.path.exists(path)
    # 判断结果
    if not isExists:
        os.makedirs(path)  
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        return False
def WriteSmallIndex(side,UnitID):
    file = open(side+"/"+UnitID+"/Index.xml","wt")
    file.write("<?xml version=\"1.0\" encoding=\"utf-8\"?>"+"\n"+"<AssetDeclaration xmlns=\"uri:ea.com:eala:asset\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\">"+"\n"+"	<Includes>"+"\n")
    file.close()
    startfile=open(side+"/"+UnitID+"/Index.xml","at")
    return startfile

def SelectSide():
    side=input("SelectSide:(A,S,J)")
    while not(side=="A"or side=="S"or side=="J"):
        side=input("SelectSide:A,S,J")
    if side=="S":
        side = "Soviet"
    elif side=="A":
        side = "Allied"
    else:
        side = "Japan"
    return side
def InputNewSide():    
    side=input("InputNewSide:")
    return side
def OpenUse(side):
    read=open(str(side+"/use.txt"),"rt")
    return read
def WriteIndex(side):
    file = open(side+"/Index.xml","wt")
    file.write("<?xml version=\"1.0\" encoding=\"utf-8\"?>"+"\n"+"<AssetDeclaration xmlns=\"uri:ea.com:eala:asset\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\">"+"\n"+"	<Includes>"+"\n")
    file.close()
    startfile=open(side+"/Index.xml","at")
    return startfile
def address(file,side):
    address = str(side+"/"+file+".xml")
    return address
def read_xml(file):
    tree = ET.parse(file)    
    return tree
def search(address,oldside,side,Newaddress):
    tree = read_xml(address)
    root = tree.getroot()
    Locomotor=[]
    Armor=[]
    weapon=[]
    idlist=[]
    alldata=[]
    for child in root:
     name=child.attrib
     if "GameObject" in child.tag:
      OBJid=name['id']
      idlist.append(OBJid)
      name['id']=name['id'].replace(oldside,side)
      for sub in child:
       if "ArmorSet" in sub.tag:
         name=sub.attrib
         KnowArmor=name['Armor']
         Armor.append(KnowArmor)
         name['Armor']=name['Armor'].replace(oldside,side)
       if "LocomotorSet" in sub.tag:
         name=sub.attrib
         KnowLocomotor=name['Locomotor']
         Locomotor.append(KnowLocomotor)
         name['Locomotor']=name['Locomotor'].replace(oldside,side)
       if "Behaviors" in sub.tag:
        for low in sub:
         if "WeaponSetUpdate" in low.tag:
          for point in low:
           for deep in point:
            if "Weapon" in deep.tag:   
              name=deep.attrib
              KnowWeapon=name['Template']
              weapon.append(KnowWeapon)
              name['Template']=name['Template'].replace(oldside,side)   
    for child in root:
      name=child.attrib
      if str(name.get('inheritFrom')) in idlist:
            name['inheritFrom']=name['inheritFrom'].replace(oldside,side)
    alldata.append(weapon)
    alldata.append(Armor)
    alldata.append(Locomotor)
    alldata.append(idlist)
    prettyXml(root, '\t', '\n')
    write_xml(tree,Newaddress+"\\"+idlist[0].replace(oldside,side)+"HJHJH.xml")
    datareplace(Newaddress+"\\"+idlist[0].replace(oldside,side)+"HJHJH.xml")
    return alldata
def weaponSet(weaponList,oldside,side,Newaddress):
    tree = read_xml("Weapon.xml")
    root = tree.getroot()
    for child in root.findall('{uri:ea.com:eala:asset}Defines'):
        root.remove(child)        
    for child in root.findall('{uri:ea.com:eala:asset}WeaponTemplate'):
      name=child.attrib
      if str(name.get('id')) in weaponList:
        name['id']=name['id'].replace(oldside,side)
        if str(name.get('inheritFrom')) in weaponList:
            name['inheritFrom']=name['inheritFrom'].replace(oldside,side)
      else:           
        if child in root.findall('{uri:ea.com:eala:asset}WeaponTemplate'):  
         root.remove(child)
    prettyXml(root, '\t', '\n')
    write_xml(tree,Newaddress+"\\"+"WeaponHJHJH.xml")
    datareplace(Newaddress+"\\"+"WeaponHJHJH.xml")
def ArmorSet(ArmorList,oldside,side,Newaddress):
    tree = read_xml("Armor.xml")
    root = tree.getroot()
    inheritFrom=[]
    for child in root.findall('{uri:ea.com:eala:asset}Defines'):
        root.remove(child)
        
    for child in root.findall('{uri:ea.com:eala:asset}ArmorTemplate'):
      name=child.attrib
      if str(name.get('id')) in ArmorList:
        name['id']=name['id'].replace(oldside,side)
        inheritFrom.append(str(name.get('inheritFrom')))
        
        if str(name.get('inheritFrom')) in ArmorList:
            name['inheritFrom']=name['inheritFrom'].replace(oldside,side)
      elif name['id'] in inheritFrom:
          print("\n")
          
      else:
        if child in root.findall('{uri:ea.com:eala:asset}ArmorTemplate'):  
         root.remove(child)      
    prettyXml(root, '\t', '\n')
    write_xml(tree,Newaddress+"\\"+"ArmorHJHJH.xml")
    datareplace(Newaddress+"\\"+"ArmorHJHJH.xml")
def SetExperienceLevel(idlist,oldside,side,Newaddress):
    tree = read_xml("ExperienceLevels.xml")
    root = tree.getroot()
    for child in root.findall('{uri:ea.com:eala:asset}ExperienceLevelTemplate'):
      name=child.attrib
      if idlist[0] in str(name.get('id')):
        name['id']=name['id'].replace(oldside,side)
        if str(name.get('inheritFrom')) in idlist:
            name['inheritFrom']=name['inheritFrom'].replace(oldside,side)
      else:           
        if child in root.findall('{uri:ea.com:eala:asset}ExperienceLevelTemplate'):  
         root.remove(child)     
    prettyXml(root, '\t', '\n')
    write_xml(tree,Newaddress+"\\"+"ExperienceLevelHJHJH.xml")
    datareplace(Newaddress+"\\"+"ExperienceLevelHJHJH.xml")    
def LocomotorSet(LocomotorList,oldside,side,Newaddress):
    tree = read_xml("Locomotor.xml")
    root = tree.getroot()
    for child in root.findall('{uri:ea.com:eala:asset}Defines'):
        root.remove(child)       
    for child in root.findall('{uri:ea.com:eala:asset}LocomotorTemplate'):
      name=child.attrib
      if str(name.get('id')) in LocomotorList:
        name['id']=name['id'].replace(oldside,side)
        if str(name.get('inheritFrom')) in LocomotorList:
            name['inheritFrom']=name['inheritFrom'].replace(oldside,side)
      else:           
        if child in root.findall('{uri:ea.com:eala:asset}LocomotorTemplate'):  
         root.remove(child)     
    prettyXml(root, '\t', '\n')
    write_xml(tree,Newaddress+"\\"+"LocomotorHJHJH.xml")
    datareplace(Newaddress+"\\"+"LocomotorHJHJH.xml")
def datareplace(address):
    Newaddress=address.replace("HJHJH","")
    file=open(address,"r")
    flie2=open(Newaddress,"w")
    line=file.readline()
    see=False
    load=False
    data=["LocomotorTemplate","WeaponTemplate","GameObject","ArmorTemplate","ExperienceLevelTemplate"]
    while line:
     for i in data:
      if i in line:
         see=True
      if "<Script>" in line:
         see=False
      if "</Script>" in line:
         see=True
     if see==True:
      c=""      
      for i in range(len(line)):
         if load==False and line[i]==" ":
          c=c+"\n"+2*"\t"+line[i]
          load=True
         elif line[i]=="\"" and line[i-1]!="=":
          c=c+line[i]+"\n"+2*"\t"
         else:
          c=c+line[i]     
      flie2.write(c)
     else:
      flie2.write(line)
     line=file.readline()
    flie2.close()
    file.close()
    os.remove(address)
def printLogicCommand(unitlist,oldside,side):
    back=[]

    for unit in unitlist:
     unit=unit.replace(oldside,side)

     print("	<LogicCommand"+"\n"+"		Type=\"UNIT_BUILD\""+"\n"+"		id=\"Command_Construct"+unit+"\">"+"\n"+"		<Object>"+unit+"</Object>"+"\n"+"	</LogicCommand>")
     back.append("<Cmd>Command_Construct"+unit+"</Cmd>")
    return back


def printAlliedLogicCommandset(setlist):
    place=[[0,1,2,3,4],[5,8,9,10,11,12],[13,14,15,16],[6,7,17,18,19,20]]


    print("	<LogicCommandSet"+"\n"+"		id=\"AlliedBarracksCommandSet\""+">")
    for i in place[0]:
     print("		"+setlist[i]+"\n")
    print("		<Cmd>Command_ConstructAlliedCommandoTech1</Cmd>")
    print("	</LogicCommandSet>"+"\n")
    print("	<LogicCommandSet"+"\n"+"		id=\"AlliedWarFactoryCommandSet\""+">")
    for i in place[1]:
     print("		"+setlist[i]+"\n")
    print("		<Cmd>Command_ConstructAlliedMCV</Cmd>			")
    print("	</LogicCommandSet>"+"\n")
    print("	<LogicCommandSet"+"\n"+"		id=\"AlliedAirfieldCommandSet\""+">")
    for i in place[2]:
     print("		"+setlist[i]+"\n")
    print("		<Cmd>Command_AlliedRecallAllAircraft</Cmd>")
    print("	</LogicCommandSet>"+"\n")
    print("	<LogicCommandSet"+"\n"+"		id=\"AlliedNavalYardCommandSet\""+">")
    for i in place[3]:
     print("		"+setlist[i]+"\n")
    print("")
    print("	</LogicCommandSet>"+"\n")
def printSovietLogicCommandset(setlist):
    place=[[0,1,2,3,4,5],[6,7,9,10,11,12],[13,14,15],[16,8,17,18]]


    print("	<LogicCommandSet"+"\n"+"		id=\"SovietBarracksCommandSet\""+">")
    for i in place[0]:
     print("		"+setlist[i]+"\n")
    print("	</LogicCommandSet>"+"\n")
    print("	<LogicCommandSet"+"\n"+"		id=\"SovietWarFactoryCommandSet\""+">")
    print("		<Cmd>Command_ConstructSovietMiner</Cmd>			")
    print("		<Cmd>Command_ConstructSovietSurveyor</Cmd>			")
    for i in place[1]:
     print("		"+setlist[i]+"\n")
    print("		<Cmd>Command_ConstructSovietMCV</Cmd>			")
    print("	</LogicCommandSet>"+"\n")
    print("	<LogicCommandSet"+"\n"+"		id=\"SovietAirfieldCommandSet\""+">")
    for i in place[2]:
     print("		"+setlist[i]+"\n")
    print("		<Cmd>Command_SovietRecallAllAircraft</Cmd>")
    print("	</LogicCommandSet>"+"\n")
    print("	<LogicCommandSet"+"\n"+"		id=\"SovietNavalYardCommandSet\""+">")
    print("		<Cmd>Command_ConstructSovietMiner_Naval</Cmd>			")
    print("		<Cmd>Command_ConstructSovietSurveyor_Naval</Cmd>			")
    for i in place[3]:
     print("		"+setlist[i]+"\n")
    print("		<Cmd>Command_ConstructSovietMCV_Naval</Cmd>			")
    print("	</LogicCommandSet>"+"\n")

##main part
NewSide=InputNewSide()
oldside=SelectSide()
Usefile = OpenUse(oldside)
line = Usefile.readline()
mkdir(NewSide)
Index = WriteIndex(NewSide)
setlist=[]
while line:
     if line.startswith("unit"):
        line = line.rstrip('\n')
        line = line.replace("unit","")        
        fileAddress=address(line,oldside)
        NewName=line.replace(oldside,NewSide)
        mkdir(NewSide+"/"+NewName)
        Index.write("		<Include type=\"all\" source=\""+NewName+"/index.xml"+"\" />"+"\n")        
        alldata=search(fileAddress,oldside,NewSide,NewSide+"/"+NewName)
        weaponSet(alldata[0],oldside,NewSide,NewSide+"/"+NewName)
        ArmorSet(alldata[1],oldside,NewSide,NewSide+"/"+NewName)
        LocomotorSet(alldata[2],oldside,NewSide,NewSide+"/"+NewName)
        SetExperienceLevel(alldata[3],oldside,NewSide,NewSide+"/"+NewName)
        command=printLogicCommand(alldata[3],oldside,NewSide)
        for i in command:
         setlist.append(i)
        SmallIndex = WriteSmallIndex(NewSide,NewName)
        SmallIndex.write("		<Include type=\"all\" source=\""+NewName+".xml"+"\" />"+"\n"+"		<Include type=\"all\" source=\"Armor.xml\" />"+"\n""		<Include type=\"all\" source=\"Weapon.xml\" />"+"\n""		<Include type=\"all\" source=\"Locomotor.xml\" />"+"\n""		<Include type=\"all\" source=\"ExperienceLevel.xml\" />"+"\n")
        SmallIndex.write("      </Includes>"+"\n"+"</AssetDeclaration>")
        SmallIndex.close()
     line = Usefile.readline()
printSovietLogicCommandset(setlist)
Index.write("      </Includes>"+"\n"+"</AssetDeclaration>")
Index.close()

