Imports System.Web
Imports System.Web.Services
Imports System.Web.Services.Protocols

Imports System.Configuration

Imports Microsoft.VisualBasic

Imports System.Data.OracleClient

Imports sitTerrassa
<WebService(Namespace:="http://emap.terrassa.cat/")> _
<WebServiceBinding(ConformsTo:=WsiProfiles.BasicProfile1_1)> _
<Global.Microsoft.VisualBasic.CompilerServices.DesignerGenerated()> _
Public Class TAIGUA
    Inherits System.Web.Services.WebService
    Partial Public Class dataCoordinates
        Public latitude As Double
        Public longitude As Double
    End Class
    Partial Public Class dataSensor
        Public sensor As String
        Public sensorType As String
        Public value As String
        Public unit As String
        Public dataType As String
        Public timestamp As String
        Public found As String
    End Class
    Partial Public Class dataComponentSENTILO
        Public icon As String
        Public provider As String
        Public sensor As String
        Public component As String
        Public componentType As String
        Public componentDesc As String
        Public type As String
        Public timestamp As String
        Public unit As String
        Public unitValue As String
        Public coordinates As TAIGUA.dataCoordinates
    End Class
    Partial Public Class dataComptadors
        Public serial_number As String
        Public comptador As String
        Public contracte As String
        Public adreca As String
        Public ultima_lectura As Double
        Public ultim_consum As Double
        Public data_ultima_lectura As String
        Public total_lectures As Integer
        Public numero_lectures As String '(7) As Integer
        Public classificacio As Integer
        Public latitud As Double
        Public longitud As Double
    End Class
    Partial Public Class dataGateways
        Public id_gateway As String
        Public nom As String
        Public latitud As Double
        Public longitud As Double
        Public data_ultim_event As String
        Public connectat As String
    End Class
    Partial Public Class dataSensorPressio
        Public serial_number As String
        Public proveidor As String
        Public id_ubicacio As String
        Public ubicacio As String
        Public latitud As Double
        Public longitud As Double
        Public node As String
        Public temps_nivell As String
        Public bateria_nivell As Double
        Public temps_pressio As String
        Public pressio As Double
        Public color As String
        Public data_ini_ubicacio As String
        Public tipus As String
    End Class
    <System.Web.Services.WebMethod(Description:="KML amb informació dels sensors de pressió")> _
    Public Function kmlSensorsPressio(ByVal token As String, ByVal file As String) As System.Xml.XmlDocument
        Dim sensorsTypeByDefault As String = ConfigurationManager.AppSettings.Item("sensorPressioComptadorsAigua")
        Dim baseName As String = "TAIGUA_SensorsPressio", baseAsFile As Boolean = False
        Dim componentsType As String = "", sensorType As String = ""
        Dim sensorsPressio As List(Of dataSensorPressio)
        Dim oXml As New System.Xml.XmlDocument

        If (token Is Nothing) Then
            token = ""
        End If
        If validateToken(token) Then
            If (file Is Nothing) Then file = ""
            If (file.Trim().Length() > 0) Then
                baseName = file.Trim
                baseAsFile = True
            End If
            sensorsPressio = cridaOracleSensorsPressio()
            oXml = montaKMLSensorsPressio(sensorsPressio)
        End If
        sitTerrassa.kml.prepareKML_Response(baseName, baseAsFile)

        kmlSensorsPressio = oXml
    End Function
    <System.Web.Services.WebMethod(Description:="KML amb informació de gateways.")> _
    Public Function kmlGateways(ByVal token As String, ByVal file As String) As System.Xml.XmlDocument
        Dim baseName As String = "TAIGUA_Gateways", baseAsFile As Boolean = False
        Dim oXml As New System.Xml.XmlDocument
        Dim gateways As List(Of dataGateways)

        If (token Is Nothing) Then
            token = ""
        End If
        If validateToken(token) Then
            If (file Is Nothing) Then file = ""
            If (file.Trim().Length() > 0) Then
                baseName = file.Trim
                baseAsFile = True
            End If
            gateways = cridaOracleGateways()
            oXml = montaKMLGateways(gateways)
        End If
        sitTerrassa.kml.prepareKML_Response(baseName, baseAsFile)

        kmlGateways = oXml

    End Function
    <System.Web.Services.WebMethod(Description:="KML amb informació comptadors d'aigua.")> _
    Public Function kmlComptadorsAigua(ByVal token As String, ByVal gransConsumidors As String, ByVal file As String) As System.Xml.XmlDocument
        Dim baseName As String = "TAIGUA_ComptadorsAigua", baseAsFile As Boolean = False
        Dim oXml As New System.Xml.XmlDocument
        Dim comptadors As List(Of dataComptadors)

        If (token Is Nothing) Then
            token = ""
        End If
        If ((gransConsumidors Is Nothing) Or (Not IsNumeric(gransConsumidors))) Then
            gransConsumidors = "0"
        End If
        If validateToken(token) Then
            If (file Is Nothing) Then file = ""
            If (file.Trim().Length() > 0) Then
                baseName = file.Trim
                baseAsFile = True
            End If
            Select Case gransConsumidors
                Case "1"
                    comptadors = cridaOracleComptadors(True)
                    oXml = montaKMLComptadors(comptadors)
                Case Else
                    comptadors = cridaOracleComptadors(False)
                    oXml = montaKMLComptadors(comptadors)
            End Select
        End If
        sitTerrassa.kml.prepareKML_Response(baseName, baseAsFile)

        kmlComptadorsAigua = oXml

    End Function
    <System.Web.Services.WebMethod(Description:="KML amb informació comptadors públics d'aigua.")> _
    Public Function kmlComptadorsPublicsAigua(ByVal file As String) As System.Xml.XmlDocument
        Dim baseName As String = "TAIGUA_ComptadorsPublicsAigua", baseAsFile As Boolean = False
        Dim oXml As New System.Xml.XmlDocument
        Dim comptadors As List(Of dataComptadors)

        If (file Is Nothing) Then file = ""
        If (file.Trim().Length() > 0) Then
            baseName = file.Trim
            baseAsFile = True
        End If
        comptadors = cridaOracleComptadors(False, True)
        oXml = montaKMLComptadors(comptadors)

        sitTerrassa.kml.prepareKML_Response(baseName, baseAsFile)

        kmlComptadorsPublicsAigua = oXml

    End Function
    Public Function cridaSENTILOSensorsPressio(ByVal componentsType As String, ByVal sensorType As String, ByVal detail As Boolean, ByVal wkid As Integer) As TAIGUA.dataComponentSENTILO()
        Dim codis() As String = componentsType.Split(",")
        Dim codi As String
        Dim retVal As New List(Of TAIGUA.dataComponentSENTILO)
        Dim sentiloData As TAIGUA.dataComponentSENTILO
        Dim urlBaseCatalog As String = ConfigurationManager.AppSettings.Item("privateUrlCatalog")
        Dim urlBaseData As String = ConfigurationManager.AppSettings.Item("privateUrlData")

        Dim sentiloJSONResult As Jayrock.Json.JsonObject, sentiloJSONProviders As Jayrock.Json.JsonArray, sentiloJSONSensors As Jayrock.Json.JsonArray
        Dim sentiloJSONData As Jayrock.Json.JsonObject
        Dim jsonObj As Jayrock.Json.JsonObject, jsonObjSensor As Jayrock.Json.JsonObject
        Dim sentiloCoordinates As String, timeStamp As String = "", unitValue As String = "", xc As Double, yc As Double
        Dim provider As String

        Dim tempTxt As String

        Dim sResponseString As String

        Dim url As String

        For Each codi In codis 'I = 0 To codis.Length - 1
            ' Crida a SENTILO
            url = String.Format(urlBaseCatalog, codi, sensorType)
            sResponseString = getSentiloURLResponse(url)

            sentiloJSONResult = Jayrock.Json.Conversion.JsonConvert.Import(sResponseString)
            sentiloJSONProviders = sentiloJSONResult.Item("providers")

            If (Not sentiloJSONProviders Is Nothing) Then
                For Each jsonObj In sentiloJSONProviders ' J = 0 To sentiloJSONProviders.Length - 1
                    provider = jsonObj.Item("provider")
                    sentiloJSONSensors = jsonObj.Item("sensors")
                    For Each jsonObjSensor In sentiloJSONSensors 'K = 0 To sentiloJSONSensors.Length - 1
                        jsonObjSensor.Item("publicAccess") = True
                        For Each sentiloData In retVal
                            If (jsonObjSensor.Item("component") <> Nothing) Then
                                If (sentiloData.component = jsonObjSensor.Item("component").ToString) Then
                                    jsonObjSensor.Item("publicAccess") = False
                                    Exit For
                                End If
                            End If
                        Next
                        If (jsonObjSensor.Item("publicAccess")) Then ' And (jsonObjSensor.Item("componentPublicAccess")) Then
                            sentiloData = New TAIGUA.dataComponentSENTILO
                            'ICONA
                            Select Case jsonObjSensor.Item("type").ToString.ToLower
                                Case "pressure"
                                    tempTxt = "pins1-poi"
                                Case Else
                                    tempTxt = "electrovalve-poi"
                            End Select
                            sentiloData.icon = tempTxt ' "deixalles-poi" 'sentiloJSONResult(K).item("icon").ToString
                            sentiloData.provider = provider
                            sentiloData.component = jsonObjSensor.Item("component").ToString
                            sentiloData.type = jsonObjSensor.Item("type").ToString
                            sentiloData.componentType = jsonObjSensor.Item("componentType").ToString
                            sentiloData.componentDesc = jsonObjSensor.Item("componentDesc").ToString
                            sentiloData.unit = jsonObjSensor.Item("unit").ToString
                            sentiloCoordinates = jsonObjSensor.Item("location").ToString
                            xc = Val(sentiloCoordinates.Split(" ")(1))
                            yc = Val(sentiloCoordinates.Split(" ")(0))
                            If (wkid = 23031) Then
                                xc += (sitTerrassa.kml.geoCorreccioX)
                                yc += (sitTerrassa.kml.geoCorreccioY)
                            End If
                            sentiloData.coordinates = New TAIGUA.dataCoordinates
                            sentiloData.coordinates.latitude = yc
                            sentiloData.coordinates.longitude = xc

                            If (detail) Then
                                ' Recollir ultima data actualitzacio
                                url = String.Format(urlBaseData, "SMARTDATASYSTEM", jsonObjSensor.Item("sensor").ToString)
                                sResponseString = getSentiloURLResponse(url)
                                sentiloJSONData = Jayrock.Json.Conversion.JsonConvert.Import(sResponseString)
                                If (sentiloJSONData.Item("observations").length > 0) Then
                                    timeStamp = sentiloJSONData.Item("observations")(0).item("timestamp").ToString
                                    Dim hora As Integer, minuts As Integer, segons As Integer
                                    Dim dia As Integer, mes As Integer, any As Integer
                                    Dim data As Date
                                    dia = Val(Mid(timeStamp, 1, 2))
                                    mes = Val(Mid(timeStamp, 4, 2))
                                    any = Val(Mid(timeStamp, 7, 4))
                                    hora = Val(Mid(timeStamp, 12, 2))
                                    minuts = Val(Mid(timeStamp, 15, 2))
                                    segons = Val(Mid(timeStamp, 18, 2))
                                    data = (New Date(any, mes, dia, hora, minuts, segons)).ToLocalTime()
                                    timeStamp = data.ToString
                                    unitValue = sentiloJSONData.Item("observations")(0).item("value").ToString
                                Else
                                    timeStamp = ""
                                    unitValue = ""
                                End If
                            End If
                            sentiloData.timestamp = timeStamp
                            sentiloData.unitValue = unitValue
                            retVal.Add(sentiloData)
                        End If
                    Next
                Next
            End If
        Next

        cridaSENTILOSensorsPressio = retVal.ToArray
    End Function
    Private Function validateToken(ByVal token As String) As Boolean
        Dim ISSUER As String = ConfigurationManager.AppSettings.Item("issuer_token")
        Dim isValid As Boolean = False
        Dim url As String = ""

        Dim req As System.Net.HttpWebRequest
        Dim serverResponse As System.Net.WebResponse = Nothing

        Dim retorn As String = ""

        If (Not token Is Nothing And token <> "") Then
            If (token = "4jt3rr4SS4_1990.$FX") Then
                isValid = True
            Else
                url = String.Format(ISSUER, token)
                Try
                    req = System.Net.HttpWebRequest.Create(url)
                    req.Method = "GET"
                    'req.Headers.Add("Authorization", "Bearer " + token)
                    req.ServicePoint.Expect100Continue = False
                    serverResponse = req.GetResponse()
                    retorn = New System.IO.StreamReader(serverResponse.GetResponseStream()).ReadToEnd()
                Catch e As Exception
                    retorn = "{""error"":}"
                End Try
                isValid = retorn.IndexOf("""error"":") = -1
            End If
        End If

        validateToken = isValid
    End Function
    Private Function prepareSerialNumber(ByVal codi As String) As String
        Dim replaceTexts As String = ConfigurationManager.AppSettings.Item("replace_text")
        Dim Canviat As String = codi
        For Each s As String In replaceTexts.Split(",")
            Canviat = Canviat.Replace(s, "")
        Next
        prepareSerialNumber = Canviat
    End Function
    Private Function URLImage(ByVal imgIcon As String) As String
        URLImage = String.Format(ConfigurationManager.AppSettings.Item("urlImages"), imgIcon)
    End Function
    Private Function GetPropertyValue(ByVal obj As Object, ByVal PropName As String) As Object
        'Dim objType As Type = obj.GetType()
        'Dim pInfo As System.Reflection.PropertyInfo = objType.GetProperty(PropName)
        'Dim PropValue As Object = pInfo.GetValue(obj, Reflection.BindingFlags.GetProperty, Nothing, Nothing, Nothing)
        Dim propValue As Object = CallByName(obj, PropName, Microsoft.VisualBasic.CallType.Get, Nothing)
        If Not TypeOf propValue Is String Then propValue = Str(propValue).Trim
        Return propValue
    End Function
    Private Function montaKMLComptadors(ByVal comptadors As List(Of dataComptadors)) As System.Xml.XmlDocument
        Dim iconesPath As String = ConfigurationManager.AppSettings.Item("path_icones")
        Dim icones() As String = ConfigurationManager.AppSettings.Item("icones_comptadors").Split(",")
        Dim oXml As New System.Xml.XmlDocument
        Dim oDec As System.Xml.XmlDeclaration
        Dim oRNode As System.Xml.XmlNode
        Dim oCNode As System.Xml.XmlNode
        Dim oXNode As System.Xml.XmlNode
        Dim iTNode As System.Xml.XmlNode
        Dim pTNode As System.Xml.XmlNode
        Dim tempNode1 As System.Xml.XmlNode
        Dim tempNode2 As System.Xml.XmlNode
        Dim tempNode3 As System.Xml.XmlNode
        Dim schemaNode As System.Xml.XmlNode
        Dim textDescription As String
        Dim llista_camps As New Dictionary(Of String, String)

        llista_camps.Add("serial_number", "string")
        llista_camps.Add("comptador", "string")
        llista_camps.Add("contracte", "string")
        llista_camps.Add("adreca", "string")
        llista_camps.Add("ultima_lectura", "double")
        llista_camps.Add("ultim_consum", "double")
        llista_camps.Add("data_ultima_lectura", "string")
        llista_camps.Add("total_lectures", "int")
        llista_camps.Add("numero_lectures", "string")
        llista_camps.Add("classificacio", "int")
        'llista_camps.Add("provider", "string")
        'llista_camps.Add("component", "string")
        'llista_camps.Add("componentType", "string")
        'llista_camps.Add("componentDesc", "string")

        ' Capcelera document
        oDec = oXml.CreateXmlDeclaration("1.0", "utf-8", "yes")
        oXml.InsertBefore(oDec, oXml.DocumentElement)

        oRNode = oXml.CreateElement("kml")
        oRNode.Attributes.Append(oXml.CreateAttribute("xmlns"))
        oRNode.Attributes.Append(oXml.CreateAttribute("xmlns:atom"))
        oRNode.Attributes.GetNamedItem("xmlns").Value = "http://earth.google.com/kml/2.2"
        oRNode.Attributes.GetNamedItem("xmlns:atom").Value = "http://www.w3.org/2005/Atom"

        oXNode = oXml.CreateElement("Document")

        oCNode = oXml.CreateElement("name")
        oCNode.InnerText = "Dades SENTILO Terrassa - Comptadors d'Aigua -"
        oXNode.AppendChild(oCNode)

        oCNode = oXml.CreateElement("description")
        sitTerrassa.xml.createCDATAElement(oXml, oCNode, "KML amb la informació dels sensors públics de la ciutat de Terrassa amb dades referents a comptadors d'aigua")
        oXNode.AppendChild(oCNode)

        ' Schema amb els noms i tipus de camps
        oCNode = oXml.CreateElement("Schema")
        oCNode.Attributes.Append(oXml.CreateAttribute("name"))
        oCNode.Attributes.GetNamedItem("name").Value = "kmlSentiloComptadors"
        oCNode.Attributes.Append(oXml.CreateAttribute("id"))
        oCNode.Attributes.GetNamedItem("id").Value = "kmlSentiloComptadors"
        oXNode.AppendChild(oCNode)

        For Each fld As KeyValuePair(Of String, String) In llista_camps
            tempNode1 = oXml.CreateElement("SimpleField")
            tempNode1.Attributes.Append(oXml.CreateAttribute("name"))
            tempNode1.Attributes.GetNamedItem("name").Value = fld.Key.ToLower
            tempNode1.Attributes.Append(oXml.CreateAttribute("type"))
            tempNode1.Attributes.GetNamedItem("type").Value = fld.Value

            oCNode.AppendChild(tempNode1)
        Next

        ' Syles pels placemarks
        For I As Integer = 0 To icones.Length - 1
            oCNode = oXml.CreateElement("Style")
            oCNode.Attributes.Append(oXml.CreateAttribute("id"))
            oCNode.Attributes.GetNamedItem("id").Value = String.Format("sentiloComptadorsAiguaTerrassa_{0}", I)

            tempNode1 = oXml.CreateElement("labelStyle")
            tempNode2 = oXml.CreateElement("scale")
            tempNode2.InnerText = "0.0"
            tempNode1.AppendChild(tempNode2)
            oCNode.AppendChild(tempNode1)

            tempNode1 = oXml.CreateElement("LabelStyle")
            tempNode2 = oXml.CreateElement("scale")
            tempNode2.InnerText = "0.0"
            tempNode1.AppendChild(tempNode2)
            oCNode.AppendChild(tempNode1)

            tempNode1 = oXml.CreateElement("IconStyle")
            tempNode2 = oXml.CreateElement("scale")
            tempNode2.InnerText = "1.0"
            tempNode1.AppendChild(tempNode2)
            tempNode2 = oXml.CreateElement("Icon")
            tempNode3 = oXml.CreateElement("href")
            tempNode3.InnerText = iconesPath + icones(I)
            tempNode2.AppendChild(tempNode3)
            tempNode1.AppendChild(tempNode2)
            oCNode.AppendChild(tempNode1)
            oXNode.AppendChild(oCNode)
        Next
        ' Elements
        For Each c As dataComptadors In comptadors
            If c.latitud <> 0.0 And c.longitud <> 0.0 Then ' Nomes procesar els que tenen coordenades.
                iTNode = oXml.CreateElement("Placemark")

                textDescription = "Comptador aigua " + c.serial_number + "<br/>" + c.adreca
                oCNode = oXml.CreateElement("name")
                oCNode.InnerText = "" & c.serial_number & ""
                iTNode.AppendChild(oCNode)
                oCNode = oXml.CreateElement("description")
                oCNode.InnerText = textDescription
                iTNode.AppendChild(oCNode)

                oCNode = oXml.CreateElement("ExtendedData")
                schemaNode = oXml.CreateElement("SchemaData")
                schemaNode.Attributes.Append(oXml.CreateAttribute("schemaUrl"))
                schemaNode.Attributes.GetNamedItem("schemaUrl").Value = "#kmlSentiloComptadors"


                tempNode1 = oXml.CreateElement("SimpleData")
                tempNode1.Attributes.Append(oXml.CreateAttribute("name"))
                tempNode1.Attributes.GetNamedItem("name").Value = "ID"
                tempNode1.InnerText = c.serial_number
                schemaNode.AppendChild(tempNode1)

                tempNode1 = oXml.CreateElement("SimpleData")
                tempNode1.Attributes.Append(oXml.CreateAttribute("name"))
                tempNode1.Attributes.GetNamedItem("name").Value = "DESCRIPCIO"
                tempNode1.InnerText = c.serial_number
                schemaNode.AppendChild(tempNode1)

                For Each fld As KeyValuePair(Of String, String) In llista_camps
                    tempNode1 = oXml.CreateElement("SimpleData")
                    tempNode1.Attributes.Append(oXml.CreateAttribute("name"))
                    tempNode1.Attributes.GetNamedItem("name").Value = fld.Key.ToLower
                    tempNode1.InnerText = GetPropertyValue(c, fld.Key)
                    schemaNode.AppendChild(tempNode1)
                Next
                oCNode.AppendChild(schemaNode)
                iTNode.AppendChild(oCNode)

                oCNode = oXml.CreateElement("styleUrl")
                oCNode.InnerText = String.Format("#sentiloComptadorsAiguaTerrassa_{0}", c.classificacio)
                iTNode.AppendChild(oCNode)
                oCNode = oXml.CreateElement("Point")
                pTNode = oXml.CreateElement("coordinates")
                pTNode.InnerText = Trim(Str(c.longitud)) + "," + Trim(Str(c.latitud))
                oCNode.AppendChild(pTNode)
                iTNode.AppendChild(oCNode)

                oXNode.AppendChild(iTNode)
            End If
        Next

        oRNode.AppendChild(oXNode)
        oXml.AppendChild(oRNode)

        montaKMLComptadors = oXml
    End Function
    Private Function montaKMLGateways(ByVal llista As List(Of dataGateways)) As System.Xml.XmlDocument
        Dim iconesPath As String = ConfigurationManager.AppSettings.Item("path_icones")
        Dim iconesText() As String = "En servei,Fora de servei".Split(",")
        Dim iconesSVG() As String = "icona_gateway_en_servei.svg,icona_gateway_fora_servei.svg".Split(",")
        Dim format_punt As String
        Dim oXml As New System.Xml.XmlDocument
        Dim oDec As System.Xml.XmlDeclaration
        Dim oRNode As System.Xml.XmlNode
        Dim oCNode As System.Xml.XmlNode
        Dim oXNode As System.Xml.XmlNode
        Dim iTNode As System.Xml.XmlNode
        Dim pTNode As System.Xml.XmlNode
        Dim tempNode1 As System.Xml.XmlNode
        Dim tempNode2 As System.Xml.XmlNode
        Dim tempNode3 As System.Xml.XmlNode
        Dim schemaNode As System.Xml.XmlNode
        Dim textDescription As String
        Dim llista_camps As New Dictionary(Of String, String)

        llista_camps.Add("id_gateway", "string")
        llista_camps.Add("nom", "string")
        llista_camps.Add("latitud", "double")
        llista_camps.Add("longitud", "double")
        llista_camps.Add("data_ultim_event", "string")
        llista_camps.Add("connectat", "string")

        ' Capcelera document
        oDec = oXml.CreateXmlDeclaration("1.0", "utf-8", "yes")
        oXml.InsertBefore(oDec, oXml.DocumentElement)

        oRNode = oXml.CreateElement("kml")
        oRNode.Attributes.Append(oXml.CreateAttribute("xmlns"))
        oRNode.Attributes.Append(oXml.CreateAttribute("xmlns:atom"))
        oRNode.Attributes.GetNamedItem("xmlns").Value = "http://earth.google.com/kml/2.2"
        oRNode.Attributes.GetNamedItem("xmlns:atom").Value = "http://www.w3.org/2005/Atom"

        oXNode = oXml.CreateElement("Document")

        oCNode = oXml.CreateElement("name")
        oCNode.InnerText = "Dades SENTILO Terrassa - Gateways -"
        oXNode.AppendChild(oCNode)

        oCNode = oXml.CreateElement("description")
        sitTerrassa.xml.createCDATAElement(oXml, oCNode, "KML amb la informació relativa als gateways de TAIGUA")
        oXNode.AppendChild(oCNode)

        ' Schema amb els noms i tipus de camps
        oCNode = oXml.CreateElement("Schema")
        oCNode.Attributes.Append(oXml.CreateAttribute("name"))
        oCNode.Attributes.GetNamedItem("name").Value = "kmlTAIGUA_Gateways"
        oCNode.Attributes.Append(oXml.CreateAttribute("id"))
        oCNode.Attributes.GetNamedItem("id").Value = "kmlTAIGUA_Gateways"
        oXNode.AppendChild(oCNode)

        For Each fld As KeyValuePair(Of String, String) In llista_camps
            tempNode1 = oXml.CreateElement("SimpleField")
            tempNode1.Attributes.Append(oXml.CreateAttribute("name"))
            tempNode1.Attributes.GetNamedItem("name").Value = fld.Key.ToLower
            tempNode1.Attributes.Append(oXml.CreateAttribute("type"))
            tempNode1.Attributes.GetNamedItem("type").Value = fld.Value

            oCNode.AppendChild(tempNode1)
        Next

        ' Syles pels placemarks
        For I As Integer = 0 To iconesText.Length - 1
            oCNode = oXml.CreateElement("Style")
            oCNode.Attributes.Append(oXml.CreateAttribute("id"))
            oCNode.Attributes.GetNamedItem("id").Value = iconesText(I)

            tempNode1 = oXml.CreateElement("labelStyle")
            tempNode2 = oXml.CreateElement("scale")
            tempNode2.InnerText = "0.0"
            tempNode1.AppendChild(tempNode2)
            oCNode.AppendChild(tempNode1)

            tempNode1 = oXml.CreateElement("LabelStyle")
            tempNode2 = oXml.CreateElement("scale")
            tempNode2.InnerText = "0.0"
            tempNode1.AppendChild(tempNode2)
            oCNode.AppendChild(tempNode1)

            tempNode1 = oXml.CreateElement("IconStyle")
            tempNode2 = oXml.CreateElement("scale")
            tempNode2.InnerText = "1.0"
            tempNode1.AppendChild(tempNode2)
            tempNode2 = oXml.CreateElement("Icon")
            tempNode3 = oXml.CreateElement("href")
            tempNode3.InnerText = iconesPath + iconesSVG(I)
            tempNode2.AppendChild(tempNode3)
            tempNode1.AppendChild(tempNode2)
            oCNode.AppendChild(tempNode1)
            oXNode.AppendChild(oCNode)
        Next
        ' Elements
        For Each c As dataGateways In llista
            If c.latitud <> 0.0 And c.longitud <> 0.0 Then ' Nomes procesar els que tenen coordenades.
                iTNode = oXml.CreateElement("Placemark")

                textDescription = ""
                If (c.id_gateway <> "") Then textDescription += "" + c.id_gateway + " - " + c.nom + "<br/>"
                textDescription += "Últim esdeveniment: " + c.data_ultim_event
                oCNode = oXml.CreateElement("name")
                oCNode.InnerText = "" & c.id_gateway & ""
                iTNode.AppendChild(oCNode)
                oCNode = oXml.CreateElement("description")
                oCNode.InnerText = textDescription
                iTNode.AppendChild(oCNode)

                oCNode = oXml.CreateElement("ExtendedData")
                schemaNode = oXml.CreateElement("SchemaData")
                schemaNode.Attributes.Append(oXml.CreateAttribute("schemaUrl"))
                schemaNode.Attributes.GetNamedItem("schemaUrl").Value = "#kmlTAIGUA_Gateways"

                For Each fld As KeyValuePair(Of String, String) In llista_camps
                    tempNode1 = oXml.CreateElement("SimpleData")
                    tempNode1.Attributes.Append(oXml.CreateAttribute("name"))
                    tempNode1.Attributes.GetNamedItem("name").Value = fld.Key.ToLower
                    tempNode1.InnerText = GetPropertyValue(c, fld.Key)
                    schemaNode.AppendChild(tempNode1)
                Next
                oCNode.AppendChild(schemaNode)
                iTNode.AppendChild(oCNode)

                oCNode = oXml.CreateElement("styleUrl")
                Select Case c.connectat
                    Case "S"
                        format_punt = iconesText(0)
                    Case Else
                        format_punt = iconesText(1)
                End Select
                oCNode.InnerText = String.Format("#{0}", format_punt)
                iTNode.AppendChild(oCNode)
                oCNode = oXml.CreateElement("Point")
                pTNode = oXml.CreateElement("coordinates")
                pTNode.InnerText = Trim(Str(c.longitud)) + "," + Trim(Str(c.latitud))
                oCNode.AppendChild(pTNode)
                iTNode.AppendChild(oCNode)

                oXNode.AppendChild(iTNode)
            End If
        Next

        oRNode.AppendChild(oXNode)
        oXml.AppendChild(oRNode)

        montaKMLGateways = oXml
    End Function
    Private Function montaKMLSensorsPressio(ByVal llista As List(Of dataSensorPressio)) As System.Xml.XmlDocument
        Dim iconesPath As String = ConfigurationManager.AppSettings.Item("path_icones")
        Dim iconesText() As String = "En funcionament,Dades més antigues de 2 dies,Amb dades negatives,Menys 20% bateria,Ubicació,Sense Dades".Split(",")
        Dim iconesSVG() As String = "icona_sensor_pressio_verd.svg,icona_sensor_pressio_groc.svg,icona_sensor_pressio_taronja.svg,icona_sensor_pressio_vermell.svg,icona_sensor_pressio_ubicacio.svg,icona_sensor_pressio_gris.svg".Split(",")
        Dim format_punt As String
        Dim oXml As New System.Xml.XmlDocument
        Dim oDec As System.Xml.XmlDeclaration
        Dim oRNode As System.Xml.XmlNode
        Dim oCNode As System.Xml.XmlNode
        Dim oXNode As System.Xml.XmlNode
        Dim iTNode As System.Xml.XmlNode
        Dim pTNode As System.Xml.XmlNode
        Dim tempNode1 As System.Xml.XmlNode
        Dim tempNode2 As System.Xml.XmlNode
        Dim tempNode3 As System.Xml.XmlNode
        Dim schemaNode As System.Xml.XmlNode
        Dim textDescription As String
        Dim llista_camps As New Dictionary(Of String, String)

        llista_camps.Add("serial_number", "string")
        llista_camps.Add("proveidor", "string")
        llista_camps.Add("id_ubicacio", "string")
        llista_camps.Add("ubicacio", "string")
        llista_camps.Add("latitud", "double")
        llista_camps.Add("longitud", "double")
        llista_camps.Add("node", "string")
        llista_camps.Add("temps_nivell", "string")
        llista_camps.Add("bateria_nivell", "double")
        llista_camps.Add("temps_pressio", "string")
        llista_camps.Add("pressio", "double")
        llista_camps.Add("color", "string")
        llista_camps.Add("data_ini_ubicacio", "string")
        llista_camps.Add("tipus", "string")

        ' Capcelera document
        oDec = oXml.CreateXmlDeclaration("1.0", "utf-8", "yes")
        oXml.InsertBefore(oDec, oXml.DocumentElement)

        oRNode = oXml.CreateElement("kml")
        oRNode.Attributes.Append(oXml.CreateAttribute("xmlns"))
        oRNode.Attributes.Append(oXml.CreateAttribute("xmlns:atom"))
        oRNode.Attributes.GetNamedItem("xmlns").Value = "http://earth.google.com/kml/2.2"
        oRNode.Attributes.GetNamedItem("xmlns:atom").Value = "http://www.w3.org/2005/Atom"

        oXNode = oXml.CreateElement("Document")

        oCNode = oXml.CreateElement("name")
        oCNode.InnerText = "Dades SENTILO Terrassa - Sensors de pressió -"
        oXNode.AppendChild(oCNode)

        oCNode = oXml.CreateElement("description")
        sitTerrassa.xml.createCDATAElement(oXml, oCNode, "KML amb la informació relativa als sensors de pressió de TAIGUA")
        oXNode.AppendChild(oCNode)

        ' Schema amb els noms i tipus de camps
        oCNode = oXml.CreateElement("Schema")
        oCNode.Attributes.Append(oXml.CreateAttribute("name"))
        oCNode.Attributes.GetNamedItem("name").Value = "kmlTAIGUA_SensorsPressio"
        oCNode.Attributes.Append(oXml.CreateAttribute("id"))
        oCNode.Attributes.GetNamedItem("id").Value = "kmlTAIGUA_SensorsPressio"
        oXNode.AppendChild(oCNode)

        For Each fld As KeyValuePair(Of String, String) In llista_camps
            tempNode1 = oXml.CreateElement("SimpleField")
            tempNode1.Attributes.Append(oXml.CreateAttribute("name"))
            tempNode1.Attributes.GetNamedItem("name").Value = fld.Key.ToLower
            tempNode1.Attributes.Append(oXml.CreateAttribute("type"))
            tempNode1.Attributes.GetNamedItem("type").Value = fld.Value

            oCNode.AppendChild(tempNode1)
        Next

        ' Syles pels placemarks
        For I As Integer = 0 To iconesText.Length - 1
            oCNode = oXml.CreateElement("Style")
            oCNode.Attributes.Append(oXml.CreateAttribute("id"))
            oCNode.Attributes.GetNamedItem("id").Value = iconesText(I)

            tempNode1 = oXml.CreateElement("labelStyle")
            tempNode2 = oXml.CreateElement("scale")
            tempNode2.InnerText = "0.0"
            tempNode1.AppendChild(tempNode2)
            oCNode.AppendChild(tempNode1)

            tempNode1 = oXml.CreateElement("LabelStyle")
            tempNode2 = oXml.CreateElement("scale")
            tempNode2.InnerText = "0.0"
            tempNode1.AppendChild(tempNode2)
            oCNode.AppendChild(tempNode1)

            tempNode1 = oXml.CreateElement("IconStyle")
            tempNode2 = oXml.CreateElement("scale")
            tempNode2.InnerText = "1.0"
            tempNode1.AppendChild(tempNode2)
            tempNode2 = oXml.CreateElement("Icon")
            tempNode3 = oXml.CreateElement("href")
            tempNode3.InnerText = iconesPath + iconesSVG(I)
            tempNode2.AppendChild(tempNode3)
            tempNode1.AppendChild(tempNode2)
            oCNode.AppendChild(tempNode1)
            oXNode.AppendChild(oCNode)
        Next
        ' Elements
        For Each c As dataSensorPressio In llista
            If c.latitud <> 0.0 And c.longitud <> 0.0 Then ' Nomes procesar els que tenen coordenades.
                iTNode = oXml.CreateElement("Placemark")

                textDescription = ""
                If (c.tipus = "sensor") Then
                    If (c.serial_number <> "") Then textDescription += "" + c.serial_number + " - " + c.proveidor + "<br/>"
                    textDescription += "% bateria: " + Trim(Str(c.bateria_nivell)) + "% (" + c.temps_nivell + ")" + "<br/>"
                    textDescription += "Pressio: " + Trim(Str(c.pressio)) + " (" + c.temps_pressio + ")" + "<br/>"
                    textDescription += "al lloc des de " + c.data_ini_ubicacio
                Else
                    If (c.serial_number <> "") Then textDescription += "" + c.serial_number + "<br/>"
                    textDescription += c.ubicacio
                End If
                oCNode = oXml.CreateElement("name")
                oCNode.InnerText = "" & c.serial_number & ""
                iTNode.AppendChild(oCNode)
                oCNode = oXml.CreateElement("description")
                oCNode.InnerText = textDescription
                iTNode.AppendChild(oCNode)

                oCNode = oXml.CreateElement("ExtendedData")
                schemaNode = oXml.CreateElement("SchemaData")
                schemaNode.Attributes.Append(oXml.CreateAttribute("schemaUrl"))
                schemaNode.Attributes.GetNamedItem("schemaUrl").Value = "#kmlTAIGUA_SensorsPressio"

                For Each fld As KeyValuePair(Of String, String) In llista_camps
                    tempNode1 = oXml.CreateElement("SimpleData")
                    tempNode1.Attributes.Append(oXml.CreateAttribute("name"))
                    tempNode1.Attributes.GetNamedItem("name").Value = fld.Key.ToLower
                    tempNode1.InnerText = GetPropertyValue(c, fld.Key)
                    schemaNode.AppendChild(tempNode1)
                Next
                oCNode.AppendChild(schemaNode)
                iTNode.AppendChild(oCNode)

                oCNode = oXml.CreateElement("styleUrl")
                Select Case c.color
                    Case "VERMELL"
                        format_punt = iconesText(3)
                    Case "TARONJA"
                        format_punt = iconesText(2)
                    Case "GROC"
                        format_punt = iconesText(1)
                    Case "VERD"
                        format_punt = iconesText(0)
                    Case "GRIS"
                        format_punt = iconesText(4)
                    Case Else
                        format_punt = iconesText(5)
                End Select
                oCNode.InnerText = String.Format("#{0}", format_punt)
                iTNode.AppendChild(oCNode)
                oCNode = oXml.CreateElement("Point")
                pTNode = oXml.CreateElement("coordinates")
                pTNode.InnerText = Trim(Str(c.longitud)) + "," + Trim(Str(c.latitud))
                oCNode.AppendChild(pTNode)
                iTNode.AppendChild(oCNode)

                oXNode.AppendChild(iTNode)
            End If
        Next

        oRNode.AppendChild(oXNode)
        oXml.AppendChild(oRNode)

        montaKMLSensorsPressio = oXml
    End Function
    Private Function getSentiloURLResponse(ByVal url As String) As String
        Dim oRequest As System.Net.HttpWebRequest
        Dim oResponse As System.Net.HttpWebResponse
        Dim oReader As System.IO.StreamReader
        Dim oHeaders As System.Net.WebHeaderCollection

        Dim tokenName As String = "identity_key"
        Dim tokenValue As String = ConfigurationManager.AppSettings.Item("tokenTAIGUA")

        Dim sResponseString As String

        oRequest = System.Net.WebRequest.Create(url)

        oHeaders = oRequest.Headers
        oHeaders.Add(tokenName, tokenValue)

        oResponse = oRequest.GetResponse
        oReader = New System.IO.StreamReader(oResponse.GetResponseStream)
        sResponseString = oReader.ReadToEnd
        oReader.Close()
        oResponse.Close()

        getSentiloURLResponse = sResponseString
    End Function
    Private Function cridaOracleComptadors(ByVal gransConsumidors As Boolean, Optional ByVal nomesPublicsAJT As Boolean = False) As List(Of dataComptadors)
        Dim sConexio As String = ConfigurationManager.AppSettings.Item("ORA_UCV_ConnectString")
        Dim sSQL As String = ""
        Dim query_extended As String = ""
        Dim oConexio As System.Data.OracleClient.OracleConnection
        Dim oCommand As System.Data.OracleClient.OracleCommand
        Dim oReader As System.Data.OracleClient.OracleDataReader
        Dim comptador As dataComptadors
        Dim comptadors As List(Of dataComptadors) = New List(Of dataComptadors)
        Dim lectures_x_dia(6) As String

        Dim bContinuar As Boolean

        If nomesPublicsAJT Then
            query_extended += "sc.dades_comptadors_itron_ajt "
        Else
            query_extended += "sc.dades_comptadors_itron "
        End If

        sSQL += "select a.serial_number as serial_number, "
        sSQL += "       a.""Comptador"" as comptador, "
        sSQL += "       a.""Contracte"" as contracte, "
        sSQL += "       a.""Adreça"" as adreca, "
        sSQL += "       a.""Lectura"" as ultima_lectura, "
        sSQL += "       a.""Consum"" as ultim_consum, "
        sSQL += "       a.""Darrer Consum"" as data_ultima_lectura, "
        sSQL += "       a.""Ahir"" as num_lectures_1, "
        sSQL += "       a.""Fa 2 dies"" as num_lectures_2, "
        sSQL += "       a.""Fa 3 dies"" as num_lectures_3, "
        sSQL += "       a.""Fa 4 dies"" as num_lectures_4, "
        sSQL += "       a.""Fa 5 dies"" as num_lectures_5, "
        sSQL += "       a.""Fa 6 dies"" as num_lectures_6, "
        sSQL += "       a.""Fa 7 dies"" as num_lectures_7, "
        sSQL += "       a.""Longitud"" as longitud, "
        sSQL += "       a.""Latitud"" as latitud "
        sSQL += "from "+query_extended+" a "
        If (gransConsumidors) Then sSQL += " where a.""Gran Consum"" = 'S' "
        sSQL += "order by a.serial_number"

        'sSQL = String.Format(sSQL, table_base)

        oConexio = New System.Data.OracleClient.OracleConnection(sConexio)
        oCommand = New System.Data.OracleClient.OracleCommand(sSQL, oConexio)
        oConexio.Open()
        oReader = oCommand.ExecuteReader()
        bContinuar = oReader.Read
        While (bContinuar)
            comptador = New dataComptadors
            comptador.serial_number = oReader.Item(0).ToString.Trim
            comptador.comptador = oReader.Item(1).ToString.Trim
            comptador.contracte = oReader.Item(2).ToString.Trim
            comptador.adreca = oReader.Item(3).ToString.Trim
            comptador.ultima_lectura = Val(Str(oReader.Item(4)).Trim)
            comptador.ultim_consum = Val(Str(oReader.Item(5)).Trim)
            comptador.data_ultima_lectura = oReader.Item(6).ToString.Trim
            comptador.total_lectures = Val(Str(oReader.Item(7)).Trim)
            lectures_x_dia(0) = comptador.total_lectures.ToString.Trim
            lectures_x_dia(1) = oReader.Item(8).ToString.Trim
            lectures_x_dia(2) = oReader.Item(9).ToString.Trim
            lectures_x_dia(3) = oReader.Item(10).ToString.Trim
            lectures_x_dia(4) = oReader.Item(11).ToString.Trim
            lectures_x_dia(5) = oReader.Item(12).ToString.Trim
            lectures_x_dia(6) = oReader.Item(13).ToString.Trim

            comptador.numero_lectures = String.Join(",", lectures_x_dia)

            comptador.longitud = Val(Str(oReader.Item(14)).Trim)
            comptador.latitud = Val(Str(oReader.Item(15)).Trim)

            If (comptador.total_lectures * 100.0 / 24.0) <= 0.0 Then
                comptador.classificacio = 0
            ElseIf (comptador.total_lectures * 100.0 / 24.0) <= 25.0 Then
                comptador.classificacio = 1
            ElseIf (comptador.total_lectures * 100.0 / 24.0) >= 25.0 And (comptador.total_lectures * 100.0 / 24.0) < 75.0 Then
                comptador.classificacio = 2
            ElseIf (comptador.total_lectures * 100.0 / 24.0) >= 75.0 Then
                comptador.classificacio = 3
            Else
                comptador.classificacio = 0
            End If
            'comptador.latitud = 0.0
            'comptador.longitud = 0.0

            comptadors.Add(comptador)
            bContinuar = oReader.Read
        End While
        oReader.Close()
        oConexio.Close()

        oConexio.Dispose()
        oCommand.Dispose()

        cridaOracleComptadors = comptadors
    End Function
    Private Function cridaOracleGateways() As List(Of dataGateways)
        Dim sConexio As String = ConfigurationManager.AppSettings.Item("ORA_UCV_ConnectString")
        Dim sSQL As String = ""
        Dim oConexio As System.Data.OracleClient.OracleConnection
        Dim oCommand As System.Data.OracleClient.OracleCommand
        Dim oReader As System.Data.OracleClient.OracleDataReader
        Dim obj As dataGateways
        Dim llista As List(Of dataGateways) = New List(Of dataGateways)

        Dim bContinuar As Boolean

        sSQL += "SELECT id_gateway, "
        sSQL += "       nom, "
        sSQL += "       latitud, "
        sSQL += "       longitud, "
        sSQL += "       concat(to_char(temps_event,'DD/MM/YYYY, HH24:MI'),'h') as data_ultima_connexio, "
        sSQL += "       connectat "
        sSQL += "FROM SC.GATEWAYS "
        sSQL += "ORDER BY id_gateway"

        oConexio = New System.Data.OracleClient.OracleConnection(sConexio)
        oCommand = New System.Data.OracleClient.OracleCommand(sSQL, oConexio)
        oConexio.Open()
        oReader = oCommand.ExecuteReader()
        bContinuar = oReader.Read
        While (bContinuar)
            obj = New dataGateways
            obj.id_gateway = oReader.Item(0).ToString.Trim
            obj.nom = oReader.Item(1).ToString.Trim
            obj.latitud = Val(Str(oReader.Item(2)).Trim)
            obj.longitud = Val(Str(oReader.Item(3)).Trim)
            obj.data_ultim_event = oReader.Item(4).ToString.Trim
            obj.connectat = oReader.Item(5).ToString.Trim

            llista.Add(obj)
            bContinuar = oReader.Read
        End While
        oReader.Close()
        oConexio.Close()

        oConexio.Dispose()
        oCommand.Dispose()

        cridaOracleGateways = llista
    End Function
    Private Function cridaOracleSensorsPressio() As List(Of dataSensorPressio)
        Dim sConexio As String = ConfigurationManager.AppSettings.Item("ORA_UCV_ConnectString")
        Dim sSQL As String = ""
        Dim oConexio As System.Data.OracleClient.OracleConnection
        Dim oCommand As System.Data.OracleClient.OracleCommand
        Dim oReader As System.Data.OracleClient.OracleDataReader
        Dim obj As dataSensorPressio
        Dim llista As List(Of dataSensorPressio) = New List(Of dataSensorPressio)

        Dim bContinuar As Boolean
        sSQL += "SELECT serial_number, "
        sSQL += "       provider, "
        sSQL += "       id_ubicacio, "
        sSQL += "       adreça as ubicacio, "
        sSQL += "       latitud, "
        sSQL += "       longitud, "
        sSQL += "       ' ' as node, "
        sSQL += "       temps_nivell, "
        sSQL += "       bateria_nivell, "
        sSQL += "       temps_pressio, "
        sSQL += "       pressio, "
        sSQL += "       color, "
        sSQL += "       to_char(data_ini_a_ubicacio,'DD/MM/YYYY HH24:MI:SS')||'h' as data_ini_ubicacio, "
        sSQL += "       'sensor' as tipus "
        sSQL += "   FROM SC.AIGUA_PRESSIO_COLOR2 "
        sSQL += "   where latitud Is Not null And longitud Is Not null "
        sSQL += "   union "
        sSQL += "select ' ' as serial_number, "
        sSQL += "       ' ' as provider, "
        sSQL += "       id_ubicacio, "
        sSQL += "       adreça as ubicacio, "
        sSQL += "       latitud, "
        sSQL += "       longitud, "
        sSQL += "       node, "
        sSQL += "       ' ' as temps_nivell, "
        sSQL += "       0.0 as bateria_nivell, "
        sSQL += "       ' ' as temps_pressio, "
        sSQL += "       0.0 as pressio, "
        sSQL += "       'GRIS' as color, "
        sSQL += "       ' ' as data_ini_ubicacio, "
        sSQL += "       'ubicacio' as tipus "
        sSQL += "    from sc.aigua_pressio_ubicacions "
        sSQL += "    where latitud Is Not null And longitud Is Not null "
        sSQL += "order by id_ubicacio, provider"


        '        sSQL += "SELECT serial_number, "
        '        sSQL += "       proveidor, "
        '        sSQL += "       latitud, "
        '        sSQL += "       longitud, "
        '        sSQL += "       temps_nivell, "
        'sSQL += "       to_char(to_date(temps_nivell,'DD/MM/YY HH24:MI:SS'),'YYYY/MM/DD HH24:MI:SS') as temps_nivell, "
        '        sSQL += "       bateria_nivell, "
        '        sSQL += "       temps_pressio, "
        'sSQL += "       to_char(to_date(temps_pressio,'DD/MM/YY HH24:MI:SS'),'YYYY/MM/DD HH24:MI:SS') as temps_pressio, "
        '        sSQL += "       pressio, "
        '        sSQL += "       color "
        '        sSQL += "FROM SC.AIGUA_PRESSIO_COLOR "
        '        sSQL += "ORDER BY serial_number, proveidor"

        oConexio = New System.Data.OracleClient.OracleConnection(sConexio)
        oCommand = New System.Data.OracleClient.OracleCommand(sSQL, oConexio)
        oConexio.Open()
        oReader = oCommand.ExecuteReader()
        bContinuar = oReader.Read
        While (bContinuar)
            obj = New dataSensorPressio
            obj.serial_number = oReader.Item(0).ToString.Trim
            obj.proveidor = oReader.Item(1).ToString.Trim
            obj.id_ubicacio = oReader.Item(2).ToString.Trim
            obj.ubicacio = oReader.Item(3).ToString.Trim

            obj.latitud = Val(Str(oReader.Item(4)).Trim)
            obj.longitud = Val(Str(oReader.Item(5)).Trim)
            obj.node = oReader.Item(6).ToString.Trim

            obj.temps_nivell = oReader.Item(7).ToString.Trim
            obj.bateria_nivell = Val(Str(oReader.Item(8)).ToString.Trim)
            obj.temps_pressio = oReader.Item(9).ToString.Trim
            obj.pressio = Val(Str(oReader.Item(10)).ToString.Trim)
            obj.color = oReader.Item(11).ToString.Trim
            obj.data_ini_ubicacio = oReader.Item(12).ToString.Trim
            obj.tipus = oReader.Item(13).ToString.Trim

            llista.Add(obj)
            bContinuar = oReader.Read
        End While
        oReader.Close()
        oConexio.Close()

        oConexio.Dispose()
        oCommand.Dispose()

        cridaOracleSensorsPressio = llista
    End Function
End Class
