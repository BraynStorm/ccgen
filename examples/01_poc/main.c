#include <stdio.h>

#include "enums.ccgen.h"

int main()
{
    puts(MyEnum_GetName(MyEnum_Alpha));
    return 0;
}