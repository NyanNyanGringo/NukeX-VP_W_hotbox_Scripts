for node in nuke.selectedNodes():
    node["mix"].setExpression("""
        [
        set label [value label]
        set index_first 0
        set pattern_exists [regexp {\d+ - \d+} $label]

        if {$pattern_exists} {} {return 1}

        while {$index_first+2 <= [llength $label]} {
            set index_last [expr $index_first + 2]
            
            if {[lindex $label $index_first] <= [value frame] && [lindex $label $index_last] >= [value frame]} {return 1}

            set index_first [expr $index_first + 3]
            }

        return 0
        ]
        """)
