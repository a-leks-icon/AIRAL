#Created: 2024-05-24
#Latest Version: 2024-05-24
#Script written by Aleksandr Schamberger (GitHub: JLEKS) as part of the AIRAL project by Ludger Paschen at ZAS Berlin.

'''For the gloss equivalency task for Nafsan: This script reads two txt files and compares, whether glosses with ":BI" appear without ":BI" . If they do, they get printed out, so that I can add them later into the cells of the respective google tables file.'''

input_path = "../../input_files/"
output_path = "../../output_files"
bi_file = "nafsan_gl_BI.txt"
gl_file = "nafsan_glosses.txt"

with open(input_path+bi_file) as bi_file:
    bis = bi_file.readlines()
with open(input_path+gl_file) as gl_file:
    gls = gl_file.readlines()

gls = [gl.removeprefix("gl: ").partition(" |")[0] for gl in gls]
gls = [gl for gl in gls if not gl.endswith(":BI")]
bis = [bi.removesuffix(":BI\n") for bi in bis]
print(bis)
print("####")
print(gls)
for bi in bis:
    if bi in gls:
        print(f"{bi}")
print("---")
for bi in bis:
    if bi in gls:
        print(f"{bi}:BI")

