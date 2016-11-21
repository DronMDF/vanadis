<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:template match="/revision">
<html>
<body>
	<h1><xsl:value-of select="project_name"/></h1>
	<p><a href='/{project_name}/settings'>Settings</a></p>

	<p>
	<xsl:if test="previous">
		<a href='/{project_name}/{previous}'><xsl:value-of select="previous"/></a>
	</xsl:if>
	&#160;<xsl:value-of select="revision"/></p>
	<p/>
	Files:<br/>
	<xsl:for-each select="file">
		<a href='/{project_name}/{name}'><xsl:value-of select="name"/></a>
			with <xsl:value-of select="issues_count"/> issues<br/>
	</xsl:for-each>
</body>
</html>
</xsl:template>
</xsl:stylesheet>
