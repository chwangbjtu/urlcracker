#include "http_def.h"

BEGIN_FS_NAMESPACE

request_t::request_t():
_method("GET"),
_path_and_parameters(""),
_path("/"),
_version("1.1"),
_paramstr("")
{
}

request_t::~request_t()
{

}

response_t::response_t():
_code("200"),
_code_info("OK"),
_version("1.1"),
_content("")
{
}

response_t::~response_t()
{

}
END_FS_NAMESPACE
