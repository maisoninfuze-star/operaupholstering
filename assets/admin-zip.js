/* Écriture d'un .zip sans compression (méthode « stored »).
   Assez pour rendre un dossier de fichiers : pas de dépendance,
   pas de CDN, et le CSP du site reste intact. */
(function(){
  'use strict';
  var T = new Int32Array(256);
  for(var n = 0; n < 256; n++){
    var c = n;
    for(var k = 0; k < 8; k++) c = (c & 1) ? (0xEDB88320 ^ (c >>> 1)) : (c >>> 1);
    T[n] = c;
  }
  function crc32(u8){
    var c = 0 ^ (-1);
    for(var i = 0; i < u8.length; i++) c = (c >>> 8) ^ T[(c ^ u8[i]) & 0xFF];
    return (c ^ (-1)) >>> 0;
  }
  function enc(s){ return new TextEncoder().encode(s); }
  function dosTime(d){
    return ((d.getHours() << 11) | (d.getMinutes() << 5) | (d.getSeconds() / 2)) & 0xFFFF;
  }
  function dosDate(d){
    return (((d.getFullYear() - 1980) << 9) | ((d.getMonth() + 1) << 5) | d.getDate()) & 0xFFFF;
  }

  /* files : [{ name:'chemin/fichier', data:Uint8Array }] */
  window.makeZip = function(files, when){
    when = when || new Date(2026, 0, 1, 12, 0, 0);
    var t = dosTime(when), dt = dosDate(when);
    var parts = [], central = [], offset = 0;

    files.forEach(function(f){
      var name = enc(f.name), data = f.data, crc = crc32(data);
      var lh = new DataView(new ArrayBuffer(30));
      lh.setUint32(0, 0x04034b50, true); lh.setUint16(4, 20, true);
      lh.setUint16(6, 0, true);          lh.setUint16(8, 0, true);
      lh.setUint16(10, t, true);         lh.setUint16(12, dt, true);
      lh.setUint32(14, crc, true);       lh.setUint32(18, data.length, true);
      lh.setUint32(22, data.length, true);
      lh.setUint16(26, name.length, true); lh.setUint16(28, 0, true);
      parts.push(new Uint8Array(lh.buffer), name, data);

      var ch = new DataView(new ArrayBuffer(46));
      ch.setUint32(0, 0x02014b50, true); ch.setUint16(4, 20, true);
      ch.setUint16(6, 20, true);         ch.setUint16(8, 0, true);
      ch.setUint16(10, 0, true);         ch.setUint16(12, t, true);
      ch.setUint16(14, dt, true);        ch.setUint32(16, crc, true);
      ch.setUint32(20, data.length, true); ch.setUint32(24, data.length, true);
      ch.setUint16(28, name.length, true);
      ch.setUint32(42, offset, true);
      central.push(new Uint8Array(ch.buffer), name);
      offset += 30 + name.length + data.length;
    });

    var cSize = central.reduce(function(a, b){ return a + b.length; }, 0);
    var eo = new DataView(new ArrayBuffer(22));
    eo.setUint32(0, 0x06054b50, true);
    eo.setUint16(8, files.length, true); eo.setUint16(10, files.length, true);
    eo.setUint32(12, cSize, true);       eo.setUint32(16, offset, true);
    return new Blob(parts.concat(central, [new Uint8Array(eo.buffer)]),
                    {type:'application/zip'});
  };
})();
