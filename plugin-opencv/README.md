### Known Issues

- when compiling OpenCV from its source, some may experience the following error. It may be caused by multi-core compiling, from `make -j8 all`. Removing `-j` resolves the issue, but takes much longer to compile.

```
#7 805.4 [ 34%] Generating test_precomp.hpp.gch/opencv_test_features2d_Release.gch
#7 805.4 [ 34%] Generating perf_precomp.hpp.gch/opencv_perf_features2d_Release.gch
#7 805.5 [ 34%] Generating precomp.hpp.gch/opencv_fuzzy_Release.gch
#7 805.6 [ 34%] Generating test_precomp.hpp.gch/opencv_test_fuzzy_Release.gch
#7 845.5 c++: internal compiler error: Killed (program cc1plus)
#7 845.5 Please submit a full bug report,
#7 845.5 with preprocessed source if appropriate.
#7 845.5 See <file:///usr/share/doc/gcc-7/README.Bugs> for instructions.
#7 845.5 make[2]: *** [modules/features2d/test_precomp.hpp.gch/opencv_test_features2d_Release.gch] Error 4
#7 845.5 modules/features2d/CMakeFiles/pch_Generate_opencv_test_features2d.dir/build.make:63: recipe for target 'modules/features2d/test_precomp.hpp.gch/opencv_test_features2d_Release.gch' failed
#7 845.7 make[2]: *** Deleting file 'modules/features2d/test_precomp.hpp.gch/opencv_test_features2d_Release.gch'
#7 845.7 make[1]: *** [modules/features2d/CMakeFiles/pch_Generate_opencv_test_features2d.dir/all] Error 2
#7 845.7 make[1]: *** Waiting for unfinished jobs....
#7 845.7 CMakeFiles/Makefile2:6075: recipe for target 'modules/features2d/CMakeFiles/pch_Generate_opencv_test_features2d.dir/all' failed
#7 875.1 [ 34%] Built target pch_Generate_opencv_features2d
#7 875.1 [ 34%] Built target pch_Generate_opencv_fuzzy
#7 875.4 [ 34%] Built target pch_Generate_opencv_test_fuzzy
#7 875.4 [ 34%] Built target pch_Generate_opencv_perf_features2d
#7 875.4 [ 34%] Built target pch_Generate_opencv_test_dnn
#7 875.5 [ 34%] Built target pch_Generate_opencv_perf_dnn
#7 875.5 Makefile:162: recipe for target 'all' failed
#7 875.5 make: *** [all] Error 2
```