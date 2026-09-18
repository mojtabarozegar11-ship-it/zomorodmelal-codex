const OfficeApp={async summary(){const r=await fetch('/api/office/summary/',{credentials:'same-origin'});if(!r.ok)throw new Error('auth_required');return r.json();}};
