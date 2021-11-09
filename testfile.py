import nicksModule2 as nick

nick.makeOrthorombicSupercellFilesFromCommandLine()

nick.addBBsToSupercellFile("orthorombicSupercell_3_3_3.mfpx",
                           "BBs/ZnPWL6.mfpx",
                           "BBs/bdc.mfpx",
                           "BBs/dabco.mfpx",
                           "BBs/ph-stub.mfpx",
                           "BBs/dabco-stub.mfpx")


nick.assignParamsToMfpxFile("orthorombicSupercell_3_3_3_withBBs.mfpx")


