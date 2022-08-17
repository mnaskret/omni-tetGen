# omni-tetGen
An omniverse extension to generate soft body meshes

![extTestBunny](https://user-images.githubusercontent.com/4333336/185104847-a556bf22-2323-4d70-8bb8-b8a57e1ec67d.gif)

## Description:

omni-tetGen uses the famous tetgen mesh generator developed by Hang Si to create tetrahedral and edge meshes for soft body simulation. The extension allows for a user-friendly drag-and-drop mechanism for input mesh data in standard .obj format. Then, it runs the python tetgen wrapper to create meshes which are converted to numpy arrays and described with additional infomration like edges rest lengths or tetrahedra volumes. Generated mesh is added to the stage with additional attributes:
- edge
- edgesRestLengths
- elem
- tetrahedronsRestVolumes
- inverseMasses

![Screenshot from 2022-08-17 13-22-38](https://user-images.githubusercontent.com/4333336/185106588-6f87d9be-c9f1-4ee4-add1-e3bff3a1538d.png)

## PBD .ogn node

Additionally, an omniverse node with a simple Position Based Dynamics algorithm implementation with CUDA kernels is attached in order to test generated meshes.

![Screenshot from 2022-08-17 13-25-31](https://user-images.githubusercontent.com/4333336/185107000-5837f3be-8540-4c5c-884f-1eb7c01b42b8.png)

## Usage

- [Install omniverse](https://www.nvidia.com/en-us/omniverse/) with e.g. create environment
- Go to: Window -> Extensions -> Gear icon -> Add extension search path: `git://github.com/mnaskret/omni-tetGen.git?branch=main`
- Find Tetrahedralizer in the list of extensions and turn it on (preferably with autoload)
- In the Tetrahedralizer window you can drop any .obj file from Omniverse Content browser, choose preferred options and generate a cool mesh
- Add a graph with PBDBasicGravity node or create your own node that utilizes mesh extra attributes to have fun with your mesh
