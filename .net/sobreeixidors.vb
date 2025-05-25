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
Public Class Sobreeixidors
    Inherits System.Web.Services.WebService
    Partial Public Class dataCoordinates
        Public latitude As Double
        Public longitude As Double
    End Class
    Partial Public Class dataSobreixidor
        Public component As String
        Public descripcio As String
        Public latitud As Double
        Public longitud As Double
        Public clase As String
        Public dayly_threshold As Integer
        Public data_darrera_lectura As String
        Public lectura As Double
    End Class
    <System.Web.Services.WebMethod(Description:="KML amb informació de sobreeixidors.")> _
    Public Function kmlSobreeixidors(ByVal token As String, ByVal file As String) As System.Xml.XmlDocument
        Dim baseName As String = "Sobreeixidors", baseAsFile As Boolean = False
        Dim oXml As New System.Xml.XmlDocument
        Dim sobreeixidors As List(Of dataSobreixidor)

        If (token Is Nothing) Then
            token = ""
        End If
        If validateToken(token) Then
            If (file Is Nothing) Then file = ""
            If (file.Trim().Length() > 0) Then
                baseName = file.Trim
                baseAsFile = True
            End If
            sobreeixidors = cridaOracleSobreeixidors()
            oXml = montaKMLSobreeixidors(sobreeixidors)
        End If
        sitTerrassa.kml.prepareKML_Response(baseName, baseAsFile)

        kmlSobreeixidors = oXml

    End Function
    Private Function validateToken(ByVal token As String) As Boolean
        Dim ISSUER As String = ConfigurationManager.AppSettings.Item("issuer_token")
        Dim BACKDOOR As String = ConfigurationManager.AppSettings.Item("backdoor_token")
        Dim isValid As Boolean = False
        Dim url As String = ""

        Dim req As System.Net.HttpWebRequest
        Dim serverResponse As System.Net.WebResponse = Nothing

        Dim retorn As String = ""

        If (Not token Is Nothing And token <> "") Then
            If (token = BACKDOOR) Then
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
    Private Function montaKMLSobreeixidors(ByVal llista As List(Of dataSobreixidor)) As System.Xml.XmlDocument
        Dim iconesPath As String = ConfigurationManager.AppSettings.Item("path_icones_sobreeixidors")
        Dim iconesText() As String = "Sense activacions,Amb activacions,Sense dades".Split(",")
        Dim iconesSVG() As String = "icon_sobreeixidor_poi_verd.svg,icon_sobreeixidor_poi_vermell.svg,icon_sobreeixidor_poi_gris.svg".Split(",")
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
        Dim nameItemText As String = "kmlTERRASSA_Sobreeixidors"

        llista_camps.Add("component", "string")
        llista_camps.Add("descripcio", "string")
        llista_camps.Add("latitud", "double")
        llista_camps.Add("longitud", "double")
        llista_camps.Add("clase", "string")
        llista_camps.Add("dayly_threshold", "integer")
        llista_camps.Add("data_darrera_lectura", "string")
        llista_camps.Add("lectura", "double")

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
        oCNode.InnerText = "Dades SENTILO Terrassa - Sobreeixidors -"
        oXNode.AppendChild(oCNode)

        oCNode = oXml.CreateElement("description")
        sitTerrassa.xml.createCDATAElement(oXml, oCNode, "KML amb la informació relativa als sobreexidors instal·lats a la ciutat")
        oXNode.AppendChild(oCNode)

        ' Schema amb els noms i tipus de camps
        oCNode = oXml.CreateElement("Schema")
        oCNode.Attributes.Append(oXml.CreateAttribute("name"))
        oCNode.Attributes.GetNamedItem("name").Value = nameItemText
        oCNode.Attributes.Append(oXml.CreateAttribute("id"))
        oCNode.Attributes.GetNamedItem("id").Value = nameItemText
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
        For Each c As dataSobreixidor In llista
            If c.latitud <> 0.0 And c.longitud <> 0.0 Then ' Nomes procesar els que tenen coordenades.
                iTNode = oXml.CreateElement("Placemark")

                textDescription = ""
                If (c.component <> "") Then textDescription += "" + c.component + " ( " + c.descripcio + ")<br/>"
                textDescription += "Darrera lectura: " + c.data_darrera_lectura
                oCNode = oXml.CreateElement("name")
                oCNode.InnerText = "" & c.component & ""
                iTNode.AppendChild(oCNode)
                oCNode = oXml.CreateElement("description")
                oCNode.InnerText = textDescription
                iTNode.AppendChild(oCNode)

                oCNode = oXml.CreateElement("ExtendedData")
                schemaNode = oXml.CreateElement("SchemaData")
                schemaNode.Attributes.Append(oXml.CreateAttribute("schemaUrl"))
                schemaNode.Attributes.GetNamedItem("schemaUrl").Value = "#" + nameItemText

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
                Select Case c.clase
                    Case "VERD"
                        format_punt = iconesText(0)
                    Case "VERMELL"
                        format_punt = iconesText(1)
                    Case Else
                        format_punt = iconesText(2)
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

        montaKMLSobreeixidors = oXml
    End Function
    Private Function cridaOracleSobreeixidors() As List(Of dataSobreixidor)
        Dim sConexio As String = ConfigurationManager.AppSettings.Item("ORA_UCV_ConnectString")
        Dim sSQL As String = ""
        Dim oConexio As System.Data.OracleClient.OracleConnection
        Dim oCommand As System.Data.OracleClient.OracleCommand
        Dim oReader As System.Data.OracleClient.OracleDataReader
        Dim obj As dataSobreixidor
        Dim llista As List(Of dataSobreixidor) = New List(Of dataSobreixidor)

        Dim bContinuar As Boolean

        sSQL += "SELECT ""component"", "
        sSQL += "       ""descripcio"", "
        sSQL += "       ""latitud"", "
        sSQL += "       ""longitud"", "
        sSQL += "       ""color"" as clase, "
        sSQL += "       concat(to_char(""darrera_lectura"",'DD/MM/YYYY, HH24:MI'),'h') as data_darrera_lectura, "
        ' sSQL += "       darrera_lectura as data_darrera_lectura, "
        sSQL += "       ""dayly_threshold"", "
        sSQL += "       ""lectura"" "
        sSQL += "FROM SC.SOFREL_GEO_COMPONENTS "
        sSQL += "ORDER BY ""component"""

        oConexio = New System.Data.OracleClient.OracleConnection(sConexio)
        oCommand = New System.Data.OracleClient.OracleCommand(sSQL, oConexio)
        oConexio.Open()
        oReader = oCommand.ExecuteReader()
        bContinuar = oReader.Read
        While (bContinuar)
            obj = New dataSobreixidor
            obj.component = oReader.Item(0).ToString.Trim
            obj.descripcio = oReader.Item(1).ToString.Trim
            obj.latitud = Val(Str(oReader.Item(2)).Trim)
            obj.longitud = Val(Str(oReader.Item(3)).Trim)
            obj.clase = oReader.Item(4).ToString.Trim
            obj.data_darrera_lectura = oReader.Item(5).ToString.Trim
            obj.dayly_threshold = IIf(IsDBNull(oReader.Item(6)), 0.0, Val(Str(oReader.Item(6)).Trim))
            obj.lectura = IIf(IsDBNull(oReader.Item(7)), 0.0, Val(Str(oReader.Item(7)).Trim))

            llista.Add(obj)
            bContinuar = oReader.Read
        End While
        oReader.Close()
        oConexio.Close()

        oConexio.Dispose()
        oCommand.Dispose()

        cridaOracleSobreeixidors = llista
    End Function
End Class
