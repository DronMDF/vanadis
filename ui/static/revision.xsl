<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:template match="/revision">
<html>
<body>
	<h1><xsl:value-of select="project_name"/></h1>
	<p><a href='/{project_name}/settings'>Settings</a></p>

	<p>
	<xsl:if test="previous">
		<xsl:choose>
		<xsl:when test="/revision/base_path">
			<a href='/{project_name}/{previous}/{base_path}'>
				<xsl:value-of select="previous"/>
			</a>
		</xsl:when>
		<xsl:otherwise>
			<a href='/{project_name}/{previous}'>
				<xsl:value-of select="previous"/>
			</a>
		</xsl:otherwise>
		</xsl:choose>
	</xsl:if>
	&#160;<xsl:value-of select="revision"/></p>
	<p/>
	Files:<br/>
	<xsl:for-each select="file">
		<xsl:sort select="name"/>
		<xsl:choose>
		<xsl:when test="/revision/base_path">
			<a href='/{/revision/project_name}/{/revision/revision}/{/revision/base_path}/{name}'>
				<xsl:value-of select="name"/>
			</a>
		</xsl:when>
		<xsl:otherwise>
			<a href='/{/revision/project_name}/{/revision/revision}/{name}'>
				<xsl:value-of select="name"/>
			</a>
		</xsl:otherwise>
		</xsl:choose>
		with <xsl:value-of select="issue_count"/> issues<br/>
	</xsl:for-each>
</body>
</html>
</xsl:template>
</xsl:stylesheet>
