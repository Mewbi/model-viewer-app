#version 120
/* simple.glsl

simple diffuse lighting based on laberts cosine law; see e.g.:
    http://en.wikipedia.org/wiki/Lambertian_reflectance
    http://en.wikipedia.org/wiki/Lambert%27s_cosine_law
*/
---VERTEX SHADER-------------------------------------------------------
#ifdef GL_ES
    precision highp float;
#endif

attribute vec3  v_pos;
attribute vec3  v_normal;

uniform float height_plan;
uniform vec4 color_component;
uniform mat4 modelview_mat;
uniform mat4 projection_mat;

varying vec4 frag_color;
varying vec4 normal_vec;
varying vec4 vertex_pos;

varying vec3 I;
varying float height;

void main (void) {

	frag_color = vec4(0, 0, 1.0, 1.0);
//	if ( v_pos.y - height_plan > - 7.0 && v_pos.y - height_plan < 7.0 ) {
//		frag_color = vec4(1.0, 0.0, 0.0, 1.0);
//	}

    //compute vertex position in eye_space and normalize normal vector
    vec4 pos = modelview_mat * vec4(v_pos,1.0);
    vec4 plan = modelview_mat * vec4(.0, height_plan, .0, 1.0);
    vertex_pos = pos;
    I = vertex_pos.xyz;
    height = plan.y;
    normal_vec = vec4(v_normal,0.0);
    gl_Position = projection_mat * pos;
}


---FRAGMENT SHADER-----------------------------------------------------
#version 120
#ifdef GL_ES
    precision highp float;
#endif

varying vec4 frag_color;
varying vec4 normal_vec;
varying vec4 vertex_pos;
varying vec3 I;
varying float height;

uniform float height_plan;
uniform mat4 normal_mat;

void main (void){
    //correct normal, and compute light vector (assume light at the eye)
    vec4 v_normal = normalize( normal_mat * normal_vec ) ;
    vec4 v_light = normalize( vec4(0,0,0,1) - vertex_pos );
    //reflectance based on lamberts law of cosine
    float theta = clamp(dot(v_normal, v_light), 0.0, 1.0);

// 6 predetermined perimeters

    if (I.y > -1.5 && I.y < -1.45 ||
    	I.y > -0.5 && I.y < -0.45 ||
		I.y > 0 && I.y < .05 ||
		I.y > .55 && I.y < .6 ||
		I.y > 1. && I.y < 1.05 ||
		I.y > 1.45 && I.y < 1.5
    ) {
    	gl_FragColor = vec4(1, 0, 0, 1) * theta;
    } else {
    	gl_FragColor = frag_color * theta;
    }

// interactive perimeter

//    if (I.y - height > -0.05 && I.y - height < 0.05) {
//		gl_FragColor = vec4(1, 0, 0, 1) * theta;
//	} else {
//		gl_FragColor = frag_color * theta;
//	}

}
