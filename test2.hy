(print #[[
damn source code
]] f"new \"test
super tetat 
" r"raw damn source" b"binary source oh yeah"
f"shit oh no
fuck "
)
; some damn comment
(fn/a [] (print "shit"))
;; some other shit
; ; some other shit
( defn func [#^int x #^bool y #^int z] (print x y z))
(defn func [int x #^bool y #^int z] (print x y z ) )

(defn func [ #^int x #^bool y #^int z ] (print x y z) (print x y z))

#{ :x 1 :s 2 :8 y #{:shit 1 :fuck 2 :oh fucking :shit oh} }
#{ :x 1 :s 2 :8 y #{:shit 1 :fuck 2 } }
