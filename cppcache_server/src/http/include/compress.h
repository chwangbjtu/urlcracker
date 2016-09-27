#ifndef __COMPRESS_H
#define __COMPRESS_H
#include "zlib.h"
#include "k_type.h"

BEGIN_FS_NAMESPACE

/*
*	compress the data in the @src buffer to the @dest buffer with gzip.
*@param dest : buffer for the compressed data
*@param dest_len : size of the @dest, if zipped successful, the actual size after zip
*@param src : data which will be compressed
*@param src_len: size of the @src
*notice:
*	@dest size must be larger than the @src size, double size if appreciate
*return:
*	Z_OK if success, Z_MEM_ERROR if there was not enough memory, 
*	Z_BUF_ERROR if there was not enough room in the output buffer.
*	the Z_XXX is defined in the zlib.h
*/

int gzip(kt::byte *dest, kt::u_long *dest_len,
				kt::byte *src, kt::u_long src_len);

/*
*	decompress the data in the @src buffer to the @dest buffer with gzip.
*@param dest : buffer for the decompressed data
*@param dest_len : size of the @dest, if unzip is successful, the actual unzipped size
*@param src : buffer for the data which will be decompressed
*@param src_len: size of the @src
*notice:
*	@dest size must be larger than the @src size, its depends on the compress
*ratio of the original data, may be 2 or more times of the compressed data size
*return:
*	Z_OK if success, Z_MEM_ERROR if there was not enough memory, 
*	Z_BUF_ERROR if there was not enough room in the output buffer, 
*	or Z_DATA_ERROR if the input data was corrupted or incomplete.
*	the Z_XXX is defined in the zlib.h
*/
int un_gzip(kt::byte *dest, kt::u_long *dest_len,
					kt::byte *src, kt::u_long src_len);

END_FS_NAMESPACE
#endif
