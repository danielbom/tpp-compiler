(ns formatter                 ;; namespace
  (:require (clojure [core] [pprint])))

(defn read-file [file] (slurp (java.io.FileReader. file)))

(def read-parse-print
  (comp clojure.pprint/pprint  ;; print
        read-string            ;; parse to a list
        read-file))            ;; read

(doseq [arg *command-line-args*] (read-parse-print arg))

