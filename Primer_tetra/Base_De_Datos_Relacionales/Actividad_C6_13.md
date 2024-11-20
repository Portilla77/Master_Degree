## Practicando el backup
- Backup completo
BACKUP DATABASE DATA_BANK
TO DISK = 'C:\Backup\DATA_BANK_FULL.bak'
WITH FORMAT, 
     NAME = 'Backup completo de DATA_BANK',
     SKIP, NOREWIND, NOUNLOAD, STATS = 10;

- Restauracion del backup
RESTORE DATABASE DATA_BANK
FROM DISK = 'C:\Backup\DATA_BANK_FULL.bak'
WITH FILE = 1, 
     NOUNLOAD, 
     REPLACE, 
     STATS = 5;

- Verificar los backups realizados
SELECT 
    database_name AS DatabaseName,
    backup_start_date AS BackupStartDate,
    backup_finish_date AS BackupFinishDate,
    backup_size/1024/1024 AS BackupSizeMB,
    physical_device_name AS BackupFilePath
FROM msdb.dbo.backupset b
JOIN msdb.dbo.backupmediafamily m
ON b.media_set_id = m.media_set_id
WHERE database_name = 'DATA_BANK'
ORDER BY backup_start_date DESC;