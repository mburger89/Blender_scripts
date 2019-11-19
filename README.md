# Blender_scripts

note: you need to have an alias set up for blender.
for bash or zsh the alias should look like this:
`alias blender="/path/to/your/blender/install"`

To run the script keyboard_gen.py script do:
`blender -P keyboard.py`
folder structure should look like this:

```text
 containing folder
 |-- 1u_keycap.obj
 |-- 1uh_homing.obj optional model
 |-- 2u_spacebar.obj optional model
```

the keycaps models should be placed in the `keycaps/` folder.
this folder needs to live in the same folder the script is run.
