// CSS__Tree_View.mjs
export default class CSS__Tree_View {
    constructor(target_element) {
        this.target_element = target_element
    }

    apply_framework() {
        if (this.target_element) {
            this.target_element.add_css_rules(this.css_rules__standard())
        }
    }

css_rules__standard() {
    return {
            ".tree-view"                         : { display        : "flex"                                    ,
                                                     flexDirection  : "column"                                  ,
                                                     padding        : "1rem"                                    ,
                                                     margin         : '1rem'                                    ,
                                                     borderRadius   : "0.375rem"                                ,
                                                     boxShadow      : "2px 2px 4px rgba(0,0,0,0.2)"             },
            ".tree-item"                         : { alignItems     : "center"                                  ,
                                                     padding        : "0.25rem"                                 ,
                                                     cursor         : "pointer"                                 },
            ".tree-item:hover"                   : { backgroundColor: "var(--table-hover-bg, rgba(0,0,0,0.04))" },
            ".tree-item-content"                 : { display        : "flex"                                    ,
                                                     alignItems     : "center"                                  ,
                                                     gap            : "0.5rem"                                  },
            ".tree-item-icon"                    : { width          : "1.5rem"                                  ,
                                                     height         : "1.5rem"                                  ,
                                                     display        : "flex"                                    ,
                                                     alignItems     : "center"                                  },
            ".tree-item-text"                    : { fontSize       : "0.9rem"                                  ,
                                                     color          : "var(--text-color, #333)"                 },
            ".tree-children"                     : { paddingLeft    : "1.5rem"                                  },
            ".tree-item-expanded"                : { transform      : "rotate(90deg)"                           },
            ".tree-folder-closed"                : { display        : "none"                                    },
            ".file-icon"                         : { color          : "var(--file-color, #6c757d)"              },
            ".folder-icon"                       : { color          : "var(--folder-color, #ffd43b)"            },
            ".tree-item-actions"                 : { marginLeft     : "auto"                                    ,
                                                     //display        : "none"                                    ,
                                                     // gap            : "0.5rem"
            },
            //".tree-item:hover .tree-item-actions": { display        : "flex"                                    },
            ".tree-item-button"                  : { padding        : "0.25rem"                                 ,
                                                     border         : "none"                                    ,
                                                     background     : "none"                                    ,
                                                     cursor         : "pointer"                                 ,
                                                     color          : "var(--action-color, #6c757d)"            },
           ".tree-item-content.selected"           : { backgroundColor: "var(--selected-bg, rgba(13, 110, 253, 0.1))" },
           ".tree-item-button:hover"            : { color          : "var(--action-hover-color, #495057)"          }
        }
    }

}