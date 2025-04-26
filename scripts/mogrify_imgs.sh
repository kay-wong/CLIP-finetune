find . -iname "*.jpg" | while read f; do convert "${f}" -strip "${f}"; done
ls * | while read f; ren "${f}" -strip "${f}"; done



find . -iname "*.jpg" | while read f; do convert "${f}" -strip "${f}"; done
# mv files if arg list too long
find tst/test_images/ -name '*.jpg' -exec mv {} ~/work/CLIP/test_images \;


mogrify "*.jpg"