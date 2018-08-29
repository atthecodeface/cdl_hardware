#include "sl_exec_file.h"
/*t t_ef_type */
typedef enum {
    ef_type_int,
    ef_type_int64,
} t_ef_type;

/*t t_ef_property */
typedef struct {
    const char *name;
    int  bit_size;
    t_ef_type ef_type;
    int  offset;
} t_ef_property;

extern void *ef_object_create( t_sl_exec_file_data *file_data, const char *name, void *owner, void *contents, t_ef_property *properties, t_sl_exec_file_method *additional_methods );
extern void *ef_object_owner(void *obj);
extern void *ef_object_contents(void *obj);
