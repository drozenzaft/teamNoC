# teamNoC
Tiffany Chen, Daniel Rozenzaft

Period 5 Computer Graphics

Final Project, 2017-18

——————————————————————————————————

Tiffany completed shading (flat/wireframe/gourand/phong) and .obj file-based polygon mesh support. Daniel completed lighting (ambient/constants/multiple lights) and modifiers for the vary command (x^n [n > 0], sin, cos, tan, ln variation).

For shading, mesh, and lighting, please use the commands as specified in MDL.spec. The syntax for shading is shading wireframe|flat|gouraud|phong. The syntax for mesh is mesh [constants] :filename. The syntax for defining lights is light name r g b x y z. The syntax for ambient light is ambient r g b. The syntax for reflective constants is constants name kar kdr ksr kag kdg ksg kab kdb ksb [r] [g] [b], where r, g, and b are the intensities. 

Special instructions are only required for the vary modifiers, which are accessed through an optional additional argument.

For x^n variation, include a numerical argument. This number can be any POSITIVE floating point value. For example, “vary bigenator 0 99 0 1 2” includes an additional argument, the 2. This would mean that vary knobs will modify with respect to y = x^2, or parabolically. Another example: if the additional argument is 0.5, the vary knobs will modify with respect to the square root function, y = x^(0.5).

For sine variation, simply include “sin” as the additional argument, like so: “vary vigenator 0 99 0 1 sin”. Sine variation works by multiplying the input x-value by pi/2 in order to fit (1,1) onto the function. This allows the knobs to neatly fit the counter while preserving sine-based modification.

For cosine variation, simply include “cos” as the additional argument, like so: “vary vigenator 0 99 0 1 cos”. Cosine variation works by multiplying the input x-value by pi/2 and subtracting it from 1 in order to fit (1,1) onto the function and account for y = cos x being a decreasing function. This allows the knobs to neatly fit the counter while maintaining increasing, cosine-based modification.

For tangent variation, simply include “tan” as the additional argument, like so: “vary vigenator 0 99 0 1 tan”. Tangent variation works by multiplying the input x-value by pi/4 in order to fit (1,1) onto the function. This allows the knobs to neatly fit the counter while preserving sine-based modification.

For natural log variation, simply include “ln” as the additional argument, like so: “vary vigenator 0 99 0 1 ln”. Natural log variation is a little more complicated: it works by multiplying the input x-value by Euler’s number, e, and subtracting the product from 2 in order to fit (1,1) onto the function. This allows the knobs to neatly fit the counter while preserving ln-based modification.