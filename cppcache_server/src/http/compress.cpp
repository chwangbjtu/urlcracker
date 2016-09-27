#include "compress.h"

BEGIN_FS_NAMESPACE

int gzip(kt::byte *dest, kt::u_long *dest_len,
		 kt::byte *src, kt::u_long src_len)
{
	z_stream_s zcompress;
	zcompress.next_in = src;
	zcompress.avail_in = src_len;
	zcompress.next_out = dest;
	zcompress.avail_out = *dest_len;
	zcompress.zalloc = (alloc_func)0;
	zcompress.zfree = (free_func)0;
	zcompress.opaque = (voidpf)0;
	zcompress.total_in = 0;
	zcompress.total_out = 0;

	int window_bits = 31; //gzip
	int compression = 9;
	int res = deflateInit2(&zcompress, compression, Z_DEFLATED, 
							window_bits, 8, Z_DEFAULT_STRATEGY);

	if (res == Z_OK)
	{
		res = deflate(&zcompress, Z_FINISH);

		if (res == Z_STREAM_END)
		{
			*dest_len = zcompress.total_out;
			deflateEnd(&zcompress);
			return Z_OK;
		}
		else
		{
			deflateEnd(&zcompress);
			return res;
		}
	}
	else
	{
		return res;
	}
}

int un_gzip(kt::byte *dest, kt::u_long *dest_len,
			kt::byte *src, kt::u_long src_len)
{
	z_stream_s zcompress;

	zcompress.next_in = src;
	zcompress.avail_in = src_len;
	zcompress.next_out = dest;
	zcompress.avail_out = *dest_len;
	zcompress.zalloc = (alloc_func)0;
	zcompress.zfree = (free_func)0;
	zcompress.opaque = (voidpf)0;
	zcompress.total_in = 0;
	zcompress.total_out = 0;

	int windowbits = 47;

	int res = inflateInit2(&zcompress, windowbits);

	if (res == Z_OK)
	{
		res = inflate(&zcompress, Z_FINISH);

		if (res == Z_STREAM_END)
		{
			*dest_len = zcompress.total_out;
			inflateEnd(&zcompress);
			return Z_OK;
		}
		else
		{
			inflateEnd(&zcompress);
			return res;
		}
	}
	else
	{
		return res;
	}
}


END_FS_NAMESPACE

