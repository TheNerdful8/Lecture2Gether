export function checkURL(url: string): {type: string, src: URL,} | undefined {
    const extensions2types: [string,string][] = 
        [['m3u8', 'application/x-mpegURL']
        ,['mp4', 'video/mp4']
        ,['ogg', 'video/ogg']
        ,['webm', 'video/webm']];
    const host2types: [string,string][] =
        [['youtube.com', 'video/youtube']
        ,['www.youtube.com', 'video/youtube']
        ,['youtu.be', 'video/youtube']];

    //Use this to extract the type from the associative arrays above
    const assoc = function<A,B>(list: [A,B][], elem: A): B|undefined {
        const res = list.find((e) => e[0] === elem);
        return res === undefined ? undefined : res[1];
    };

    let host, extension, urlobj;
    try {
        urlobj = new URL(url);
        host = urlobj.hostname;
        extension = urlobj.pathname.split('.').pop();
    } catch { 
        return undefined;
    }

    let type;
    //check type based on extension first
    type = assoc(extensions2types, extension);
    //check type based on hostname next
    if (type === undefined) type = assoc(host2types, host);
    if (type === undefined) return undefined;

    return {
        type: type,
        src: urlobj,
    };
}
