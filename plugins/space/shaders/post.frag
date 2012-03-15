#version 120

uniform sampler2D texture;

void main()
{

  vec4 color = texture2D( texture, gl_TexCoord[0].st ) * 0.4;
  const float m = 600;
  for( int i = 1; i < 3; i++ )
  {
    color += texture2D( texture, gl_TexCoord[0].st + vec2( i, 0 )/m );
    color += texture2D( texture, gl_TexCoord[0].st + vec2( -i, 0 )/m );
    color += texture2D( texture, gl_TexCoord[0].st + vec2( 0, i )/m );
    color += texture2D( texture, gl_TexCoord[0].st + vec2( 0, -i )/m );
    color += texture2D( texture, gl_TexCoord[0].st + vec2( i, -i )/m );
    color += texture2D( texture, gl_TexCoord[0].st + vec2( -i, -i )/m );
    color += texture2D( texture, gl_TexCoord[0].st + vec2( -i, i )/m );
    color += texture2D( texture, gl_TexCoord[0].st + vec2( i, i )/m );
  }
  gl_FragColor = color/(8*2);
}
