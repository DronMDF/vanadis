<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:template match="/">
<html>
<body>
	<h1><xsl:value-of select="project_name"/></h1>
	<p><a href='/{{project.name}}/import'>Upload report file</a></p>
	<p><a href='/{{project.name}}/settings'>Settings</a></p>

	<p>
	<xsl:if test="previous">
		<a href='/{{project.name}}/{{previous}}'>{{previous}}</a>
	</xsl:if> {{revision}}</p>
	<p/>
	Files:<br/>
	<xsl:for-each select="file">
		<a href='/{{project.name}}/{{file.name}}'><xsl:value-of select="name"/></a>
			with <xsl:value-of select="issues_count"/> issues<br/>
	</xsl:for-each>
</body>
</html>
</xsl:template>
</xsl:stylesheet>
